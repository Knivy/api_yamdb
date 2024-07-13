"""Модель пользователя."""

import re

from django.db import models  # type: ignore
from django.contrib.auth.models import AbstractUser  # type: ignore
from django.core.validators import MaxLengthValidator  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore

from .constants import (EMAIL_MAX_LENGTH, NAME_MAX_LENGTH)


class Role(models.TextChoices):
    """Роли пользователя."""

    USER = 'user', _('Пользователь')
    MODERATOR = 'moderator', _('Модератор')
    ADMIN = 'admin', _('Администратор')


def get_role_max_length():
    """Длина поля роли."""
    return max(len(role[0]) for role in Role.choices)


def validate_username(username):
    """Проверка логина."""
    if username.lower() == 'me':
        raise ValidationError(
            'Нельзя назвать логин "me".'
        )
    if len(username) > NAME_MAX_LENGTH:
        raise ValidationError(
            f'Длина логина не должна превышать '
            f'{NAME_MAX_LENGTH} символов.'
        )
    if not re.fullmatch(r'^[\w\d\.@+-]+$', username):
        raise ValidationError(
            'Логин содержит недопустимые символы.'
        )
    return username


def validate_email(email):
    """Проверка email."""
    if len(email) > EMAIL_MAX_LENGTH:
        raise ValidationError(
            'Email слишком длинный.'
        )
    return email


class YamdbUser(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        verbose_name='Логин',
        max_length=NAME_MAX_LENGTH,
        validators=(MaxLengthValidator,
                    validate_username),
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=EMAIL_MAX_LENGTH,
        validators=(MaxLengthValidator,
                    validate_email),
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=NAME_MAX_LENGTH,
        validators=(MaxLengthValidator,),
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=NAME_MAX_LENGTH,
        validators=(MaxLengthValidator,),
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=Role.choices,
        max_length=get_role_max_length(),
        validators=(MaxLengthValidator,),
        default=Role.USER,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_superuser_or_admin(self):
        return self.is_superuser or self.role == Role.ADMIN

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR

    @property
    def is_moderator_or_higher(self):
        return self.role == Role.MODERATOR or self.is_superuser_or_admin

    @property
    def is_user(self):
        return self.role == Role.USER
