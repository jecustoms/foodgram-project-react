from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(
        'first name',
        max_length=30,
        blank=False,
        help_text='Required. 30 characters or fewer.'
    )
    last_name = models.CharField(
        'last name',
        max_length=150,
        blank=False,
        help_text='Required. 150 characters or fewer.'
    )
    email = models.EmailField(
        'email address',
        blank=False,
        unique=True,
        help_text='Required.'
    )

    class Meta:
        app_label = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
