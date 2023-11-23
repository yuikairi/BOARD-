from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
  path('signup/', views.SignUpView.as_view(), name='signup'),
  path('signup_success/', views.SignUpSuccessView.as_view(), name='signup_success'),
  path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
  path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
  path('edit_profile/', views.edit_profile, name='edit_profile'),
  path('profile/', views.profile, name='profile'),
  path('delete_profile/', views.delete_profile, name='delete_profile'),
  ]