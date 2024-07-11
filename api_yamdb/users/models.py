"""Модель пользователя."""

from django.db import models  # type: ignore
from django.contrib.auth.models import AbstractUser  # type: ignore

from .constants import (EMAIL_MAX_LENGTH, NAME_MAX_LENGTH,
                        ROLE_CHOICES, ROLE_MAX_LENGTH)


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
        max_length=ROLE_MAX_LENGTH,
        default='user',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_superuser or self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
