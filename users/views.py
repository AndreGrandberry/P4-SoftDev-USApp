from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView
from django.db.models import Q
from reviews.models import Review

# Create your views here.
class SignupView(View):

    def get(self, request):
        # redirect authenticated users to profile
        if request.user.is_authenticated:
            return redirect('users:profile')
        return render(request, 'users/signup.html', {'form_data': {}})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('users:profile')

        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        errors = []

        User = get_user_model()
        if not username:
            errors.append('Username is required.')
        elif User.objects.filter(username=username).exists():
            errors.append('This username is already taken.')

        if not password1 or not password2:
            errors.append('Both password fields are required.')
        elif password1 != password2:
            errors.append('Passwords do not match.')

        if errors:
            return render(request, 'users/signup.html', {
                'errors': errors,
                'form_data': {'username': username},
            })

        user = User.objects.create_user(username=username, password=password1)
        return render(request, 'users/signup.html', {
            'created': True,
            'username': user.username,
        })


class ProfileView(LoginRequiredMixin, TemplateView):
    """Display the logged-in user's profile page, showing their info,
       reviews, and follower/following counts.
    """

    template_name = 'users/profile.html'
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        """Return context data for the profile page,
           including follower/following counts and the user's reviews.
        """
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        # follower/following counts for the logged-in user
        User = get_user_model()
        user = self.request.user
        if user.is_authenticated:
            context['following_count'] = user.following.count()
            # followers are users who have this user in their following m2m
            context['followers_count'] = User.objects.filter(following__pk=user.pk).count()
            # include the current user's reviews on their profile page
            from reviews.models import Review
            context['reviews'] = Review.objects.filter(user=user).order_by('-created')
            # lists for UI: who the user follows, and who follows the user
            context['following_list'] = list(user.following.all())
            context['followers_list'] = list(User.objects.filter(following__pk=user.pk).order_by('first_name', 'last_name'))
            # ids of users the current user follows (for button state)
            context['following_ids'] = list(user.following.values_list('pk', flat=True))
        else:
            context['following_count'] = 0
            context['followers_count'] = 0
            context['reviews'] = []
        return context


class FollowToggleView(LoginRequiredMixin, View):
    """Toggle following/unfollowing another user. Requires login.
        Redirects back to the referring page after toggling.
    """

    def post(self, request, user_id):
        User = get_user_model()
        target = User.objects.filter(pk=user_id).first()
        if not target or target == request.user:
            messages.error(request, 'Invalid user.')
            return redirect('users:profile')

        # toggle follow
        if request.user.following.filter(pk=target.pk).exists():
            request.user.following.remove(target)
            messages.success(request, f'You unfollowed {target.full_name}.')
        else:
            request.user.following.add(target)
            messages.success(request, f'You are now following {target.full_name}.')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('users:profile')))


class UserDetailView(LoginRequiredMixin, DetailView):
    """Display another user's public profile.

    Adds the following context keys:
    - is_following: whether the current user follows the profile user
    - reviews: the profile user's reviews (ordered newest first)
    - following_count / followers_count: counts for the profile user
    """
    model = get_user_model()
    template_name = 'users/user_detail.html'
    context_object_name = 'profile_user'
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        """Add follow relationship and reviews to the template context."""
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        is_following = False
        if user.is_authenticated and user != self.object:
            is_following = user.following.filter(pk=self.object.pk).exists()
        ctx['is_following'] = is_following
        # include the profile user's reviews
        ctx['reviews'] = Review.objects.filter(user=self.object).order_by('-created')
        # follower/following counts for the profile user
        User = get_user_model()
        ctx['following_count'] = self.object.following.count()
        ctx['followers_count'] = User.objects.filter(following__pk=self.object.pk).count()
        # provide lists for the UI (who the profile user follows, and who follows them)
        ctx['following_list'] = list(self.object.following.all())
        ctx['followers_list'] = list(
            User.objects.filter(following__pk=self.object.pk).order_by('first_name', 'last_name'))
        # ids of users the current request.user follows (used for button state)
        if self.request.user.is_authenticated:
            ctx['following_ids'] = list(self.request.user.following.values_list('pk', flat=True))
        else:
            ctx['following_ids'] = []
        return ctx


class UserSearchView(LoginRequiredMixin, TemplateView):
    """Search for users by name or username. Requires login.

    """
    template_name = 'users/search_results.html'

    def get(self, request, *args, **kwargs):
        """Handle GET requests to perform the search and render results."""
        q = request.GET.get('q', '').strip()
        results = []
        results_info = []
        if q:
            User = get_user_model()
            results = User.objects.filter(
                Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(username__icontains=q)
            ).order_by('first_name', 'last_name')

            # Prepare counts for each result user
            for u in results:
                reviews_count = u.review_set.count()
                following_count = u.following.count()
                followers_count = User.objects.filter(following__pk=u.pk).count()
                results_info.append({
                    'user': u,
                    'reviews_count': reviews_count,
                    'following_count': following_count,
                    'followers_count': followers_count,
                })

        following_ids = []
        if request.user.is_authenticated:
            following_ids = list(request.user.following.values_list('pk', flat=True))

        return render(request, self.template_name,
                      {'query': q, 'results': results_info, 'following_ids': following_ids})

