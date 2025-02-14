from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogout,UserAccountUpdateView, UserPasswordChangeView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/',UserRegistrationView.as_view(), name='register'),
    path('login/',UserLoginView.as_view(), name='login'),
    path('logout/',UserLogout.as_view(), name='logout'),
    path('profile/',UserAccountUpdateView.as_view(), name='profile' ),
    path('profile/password_change/',UserPasswordChangeView.as_view(), name='password_change'),
]