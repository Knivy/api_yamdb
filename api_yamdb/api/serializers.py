"""Сериализаторы."""

from rest_framework import serializers  # type: ignore
from rest_framework.relations import SlugRelatedField  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from rest_framework.validators import UniqueTogetherValidator  # type: ignore

from reviews.models import Category, Genre

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
