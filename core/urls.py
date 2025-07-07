from django.urls import path
from .views import LoginView, LogoutView, RegisterView, auth_view

urlpatterns = [
    path('auth/', auth_view, name="auth"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]