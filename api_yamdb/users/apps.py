"""Настройки приложения."""

from django.apps import AppConfig  # type: ignore


class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи'
