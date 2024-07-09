"""Модели."""

from django.db import models  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from api_yamdb.constants import (MAX_NAME_LENGTH, MAX_SLUG_LENGTH,
                                 MIN_SCORE, MAX_SCORE)

User = get_user_model()


class BaseNameModel(models.Model):
    """Базовая модель с именем."""

    name = models.CharField(max_length=MAX_NAME_LENGTH,
                            verbose_name='Название')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class BaseSlugModel(models.Model):
    """Базовая модель со слагом."""

    slug = models.SlugField(unique=True, max_length=MAX_SLUG_LENGTH,
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


class BaseTextModel(models.Model):
    """Базовая текстовая модель."""

    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class Review(BaseTextModel):
    """Отзывы."""

    score = models.PositiveSmallIntegerField(
        choices=tuple((i, str(i)) for i in range(MIN_SCORE,
                                                 MAX_SCORE + 1)),
        verbose_name='Оценка')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Произведение')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)


class Comment(BaseTextModel):
    """Комментарии."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)
