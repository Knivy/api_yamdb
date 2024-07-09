"""Модели."""

from django.db import models  # type: ignore
from django.contrib.auth.models import AbstractUser  # type: ignore
from django.conf import settings  # type: ignore


class CastomUser(AbstractUser):
    """Модель пользователя"""

    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
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
        max_length=150,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    """Категории."""

    name = models.CharField(max_length=settings.MAX_NAME_LENGTH,
                            verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=settings.MAX_SLUG_LENGTH,
                            verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры."""

    name = models.CharField(max_length=settings.MAX_NAME_LENGTH,
                            verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=settings.MAX_SLUG_LENGTH,
                            verbose_name='Слаг')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения искусства."""

    name = models.CharField(max_length=settings.MAX_NAME_LENGTH,
                            verbose_name='Название')
    year = models.PositiveSmallIntegerField(verbose_name='Год')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre, related_name='titles',
        verbose_name='Жанры', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name='titles',
        verbose_name='Категория', blank=True, null=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name
