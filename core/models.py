from datetime import datetime
from typing import LiteralString
from django.db import models
from django.contrib.auth.models import User
import string
import random


# LiteralString is used to indicate that the string is a literal and not a regular string. helps with type checking, and saves from injection attacks
def generate_code(length=6) -> LiteralString:
    characters = string.ascii_letters + string.digits
    while True:
        code: LiteralString = "".join(random.choices(characters, k=length))
        if not Room.objects.filter(code=code).exists():
            return code


class Room(models.Model):
    code = models.CharField(max_length=10, unique=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Room {self.code} hosted by {self.host.username}"


class RoomUser(models.Model):
    # related_name ref -> https://docs.djangoproject.com/en/5.2/ref/models/fields/#django.db.models.ForeignKey.related_name
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="participants"
    )  # here, related_name basically tells which user has joined this specific room.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="joined_rooms"
    )  # related_name allows reverse lookup from User to RoomUser, basically tells which rooms are joined by that user.
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} in {self.room.code}"

    # This ensures that a user can only join a room once
    class Meta:
        unique_together = ("room", "user")
