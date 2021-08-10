from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField('E-mail', max_length=254, unique=True)
    username = models.CharField('Никнейм', max_length=150)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name'
    ]

    objects = CustomUserManager()

    def __str__(self):
        return self.username
