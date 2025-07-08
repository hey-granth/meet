from django.urls import path
from .views import LoginView, LogoutView, RegisterView, auth_view, CreateRoomView, JoinRoomView, RoomDetailView

urlpatterns = [
    path('auth/', auth_view, name="auth"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create-room/', CreateRoomView.as_view(), name='create-room'),
    path('join-room/', JoinRoomView.as_view(), name='join-room'),
    path('room/<str:code>/', RoomDetailView.as_view(), name='room-detail'),
]
