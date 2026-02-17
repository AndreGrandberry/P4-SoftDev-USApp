from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model

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


