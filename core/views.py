from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from typing import Dict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def auth_view(request) -> Response:
    content: Dict[str, str] = {
        "user": str(request.user),
        "auth": str(request.auth),
    }
    return Response(content)


class RegisterView(APIView):
    def post(self, request) -> Response:
        """
        Handle user registration.
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
    def post(self, request) -> Response:
        """
        Handle user login.
        """
        username: str = request.data.get("username")
        password: str = request.data.get("password")

        user: User|None = authenticate(username=username, password=password)
        if user:
            login(request, user)    # creates a session and logs in the user
            return Response({"message": "Login successful."}, status=HTTP_200_OK)

        return Response({"error": "Invalid credentials."}, status=HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request) -> Response:
        """
        Handle user logout.
        """
        if request.user.is_authenticated:
            logout(request)
            return Response({"message": "Logout successful."}, status=HTTP_200_OK)

        return Response({"error": "User is not authenticated."}, status=HTTP_401_UNAUTHORIZED)