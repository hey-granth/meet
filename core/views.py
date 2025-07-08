from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from typing import Dict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Room


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def auth_view(request) -> Response:
    """
    View to return user and auth information.
    :param request: WSGIRequest object containing user and auth information
    :return: Response with user and auth information
    """
    content: Dict[str, str] = {
        "user": str(request.user),
        "auth": str(request.auth),
    }
    return Response(content)


class RegisterView(APIView):
    """
    View to handle user registration.
    """
    def post(self, request) -> Response:
        """
        Handle user registration.
        :param request: {username, password}
        :return: Response with success or error message
        """
        username: str = request.data.get("username")
        password: str = request.data.get("password")

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=HTTP_400_BAD_REQUEST)

        user: User = User.objects.create_user(username=username, password=password)
        user.save()
        return Response({"message": "User created successfully."}, status=HTTP_201_CREATED)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """
    View to handle user login.
    """
    def post(self, request) -> Response:
        """
        Handle user login.
        :param request: {username, password}
        :return: Response with success or error message
        """
        username: str = request.data.get("username")
        password: str = request.data.get("password")

        user: User|None = authenticate(username=username, password=password)
        if user:
            login(request, user)    # creates a session and logs in the user
            return Response({"message": "Login successful."}, status=HTTP_200_OK)

        return Response({"error": "Invalid credentials."}, status=HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    View to handle user logout.
    """
    def post(self, request) -> Response:
        """
        Handle user logout.
        :param request: {user}
        :return: Response with success or error message
        """
        if request.user.is_authenticated:
            logout(request)
            return Response({"message": "Logout successful."}, status=HTTP_200_OK)

        return Response({"error": "User is not authenticated."}, status=HTTP_401_UNAUTHORIZED)


@permission_classes([IsAuthenticated])
class CreateRoomView(APIView):
    """
    View to create a new room.
    """
    def post(self, request) -> Response:
        """
        Create a new room.
        :param request: {user, data}
        :return: Response with success or error message
        """
        user: User = request.user
        code: str = request.data.get("code")

        if not code:
            return Response({"error": "Room code is required."}, status=HTTP_400_BAD_REQUEST)

        if Room.objects.filter(code=code).exists():
            return Response({"error": "Room code already exists."}, status=HTTP_400_BAD_REQUEST)

        room: Room = Room.objects.create(code=code, host=user)
        return Response({"message": f"Room {room.code} created successfully."}, status=HTTP_201_CREATED)


@permission_classes([IsAuthenticated])
class JoinRoomView(APIView):
    """
    View to join an existing room.
    """
    def post(self, request) -> Response:
        """
        Join an existing room by code.
        :param request: {user, data}
        :return: Response with success or error message
        """
        user: User = request.user
        code: str = request.data.get("code")

        if not code:
            return Response({"error": "Room code is required."}, status=HTTP_400_BAD_REQUEST)

        try:
            room: Room = Room.objects.get(code=code)
        except Room.DoesNotExist:
            return Response({"error": "Room does not exist."}, status=HTTP_404_NOT_FOUND)

        if room.participants.filter(user=user).exists():
            return Response({"error": "You have already joined this room."}, status=HTTP_400_BAD_REQUEST)

        room.participants.create(user=user)     # could do this coz i used reverse relationship in RoomUser model (related_name)
        return Response({"message": f"You have joined room {room.code}."}, status=HTTP_200_OK)

