"""Сериализаторы."""

from rest_framework import serializers  # type: ignore
from rest_framework.relations import SlugRelatedField  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from rest_framework.validators import UniqueTogetherValidator  # type: ignore

from reviews.models import Category, Genre, Title

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

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genre')


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
