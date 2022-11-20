from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from User.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Represents the user."""

    login = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=40, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_support = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


    def __str__(self):
        user = f"Login: {self.login}. Is support: {self.is_support}"
        return user