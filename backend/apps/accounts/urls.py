from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UserProfileView, get_csrf_token

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/user/', UserProfileView.as_view(), name='user-profile'),
    path('auth/csrf/', get_csrf_token, name='get_csrf_token'),
]