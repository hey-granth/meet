from datetime import datetime
from typing import LiteralString
from django.db import models
from django.contrib.auth.models import User
import string
import random


def generate_code(length=6) -> LiteralString:
    characters = string.ascii_letters + string.digits
    while True:
        code: LiteralString = ''.join(random.choices(characters, k=length))
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


    def __str__(self):
        return f"Room {self.code} hosted by {self.host.username}"


