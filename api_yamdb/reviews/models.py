"""Модели."""

from django.db import models  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.conf import settings  # type: ignore

User = get_user_model()


class BaseNameModel(models.Model):
    """Базовая модель с именем."""

    name = models.CharField(max_length=settings.MAX_NAME_LENGTH,
                            verbose_name='Название')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class BaseSlugModel(models.Model):
    """Базовая модель с слагом."""

    slug = models.SlugField(unique=True, max_length=settings.MAX_SLUG_LENGTH,
                            verbose_name='Слаг')

    class Meta:
        abstract = True


class Category(BaseNameModel, BaseSlugModel):
    """Категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseNameModel, BaseSlugModel):
    """Жанры."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(BaseNameModel):
    """Произведения искусства."""

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
