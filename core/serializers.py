from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Room, RoomUser


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["code", "host", "created_at"]
        read_only_fields = ["code", "host", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
        read_only_fields = ["id", "email"]


class RoomUserSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = RoomUser
        fields = ["room", "user", "joined_at"]
        read_only_fields = ["room", "user", "joined_at"]
