from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Super Admin'
        USER = 'user', 'User'

    role = models.CharField(max_length=16, choices=Roles.choices, default=Roles.USER)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
