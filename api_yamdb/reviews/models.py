"""Модели."""

from django.db import models  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from .constants import (MAX_NAME_LENGTH, MAX_SLUG_LENGTH,
                        MIN_SCORE, MAX_SCORE)


User = get_user_model()


class BaseNameModel(models.Model):
    """Базовая модель с именем."""

    name = models.CharField(max_length=MAX_NAME_LENGTH,
                            verbose_name='Название')

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class BaseNameSlugModel(BaseNameModel):
    """Базовая модель с именем и слагом."""

    slug = models.SlugField(unique=True, max_length=MAX_SLUG_LENGTH,
                            verbose_name='Слаг')

    class Meta(BaseNameModel.Meta):
        abstract = True


class Category(BaseNameSlugModel):
    """Категории."""

    class Meta(BaseNameSlugModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseNameSlugModel):
    """Жанры."""

    class Meta(BaseNameSlugModel.Meta):
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

    class Meta(BaseNameModel.Meta):
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class BaseTextModel(models.Model):
    """Базовая текстовая модель."""

    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

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

    class Meta(BaseTextModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            # К одному произведению можно только один обзор.
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_title_author'),
        ]


class Comment(BaseTextModel):
    """Комментарии."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор')

    class Meta(BaseTextModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
