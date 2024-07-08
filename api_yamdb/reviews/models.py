from django.db import models  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.conf import settings  # type: ignore

User = get_user_model()


class BaseNameModel(models.Model):
    """Базовая модель с полем имени."""

    name = models.CharField(max_length=settings.MAX_STRING_IN_DATABASE,
                            verbose_name='Название')

    def __str__(self):
        return self.name
 

class BaseSlugModel(models.Model):
    """Базовая модель с полем слага."""

    slug = models.SlugField(unique=True,
                            verbose_name='Слаг')


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
    genre = models.ForeignKey(
        Genre, on_delete=models.DO_NOTHING, related_name='titles',
        verbose_name='Жанр', blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name='titles',
        verbose_name='Категория', blank=True, null=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)
