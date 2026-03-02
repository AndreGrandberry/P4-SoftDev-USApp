from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignupView, ProfileView, UserDetailView, UserSearchView, FollowToggleView

app_name = 'users'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/users/login'), name='logout'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='profile_detail'),
    path('search/', UserSearchView.as_view(), name='search'),
    path('follow/<int:user_id>/', FollowToggleView.as_view(), name='follow'),
]