"""Модель пользователя."""

from django.db import models
from django.contrib.auth.models import AbstractUser

from .constants import EMAIL_MAX_LENGTH, NAME_MAX_LENGTH, ROLE_CHOICES


class YamdbUser(AbstractUser):
    """Модель пользователя"""

    username = models.CharField(
        verbose_name='Логин',
        max_length=NAME_MAX_LENGTH,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLE_CHOICES,
        default='user',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username