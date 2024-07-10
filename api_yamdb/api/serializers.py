"""Сериализаторы."""

from rest_framework import serializers  # type: ignore
from rest_framework.relations import SlugRelatedField  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
import numpy as np

from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор произведений на запись."""

    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genre', 'rating')

    def get_rating(self, obj):
        """Расчёт рейтинга."""
        return np.mean((score for score
                        in obj.reviews.values_list('score', flat=True)))


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор произведений на чтение."""

    # Надо еще добавить rating.

    category = CategorySerializer()
    genre = GenreSerializer(
        many=True,
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор обзоров."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
