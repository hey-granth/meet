from django.db import models
from django.contrib.auth.models import AbstractUser

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)

