from django.db import models  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.conf import settings  # type: ignore

User = get_user_model()


class Category(models.Model):
    """Категории."""

    name = models.CharField(max_length=settings.MAX_STRING_IN_DATABASE,
                            verbose_name='Название')
    slug = models.SlugField(unique=True,
                            verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры."""

    name = models.CharField(max_length=settings.MAX_STRING_IN_DATABASE,
                            verbose_name='Название')
    slug = models.SlugField(unique=True,
                            verbose_name='Слаг')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения искусства."""

    name = models.CharField(max_length=settings.MAX_STRING_IN_DATABASE,
                            verbose_name='Название')
    year = models.PositiveSmallIntegerField(verbose_name='Год')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre, related_name='titles',
        verbose_name='Жанры', blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name='titles',
        verbose_name='Категория', blank=True, null=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name