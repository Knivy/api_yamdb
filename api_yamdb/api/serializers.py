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

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def to_representation(self, instance):
        """Представление объекта."""
        view = self.context.get('view')
        if not view:
            raise serializers.ValidationError('Нет view.')
        return TitleReadSerializer().to_representation(instance)


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор произведений на чтение."""

    category = CategorySerializer()
    genre = GenreSerializer(
        many=True,
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category')

    def get_rating(self, obj):
        """Расчёт рейтинга."""
        scores = obj.reviews.values_list('score', flat=True)
        return int(np.mean([score for score
                           in scores])) if scores else None


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор с полем автора."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        abstract = True


class ReviewSerializer(AuthorSerializer):
    """Сериализатор обзоров."""

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')

    def validate(self, data_to_validate):
        """Проверка единственности отзыва."""
        view = self.context.get('view')
        if not view:
            raise serializers.ValidationError('Нет view.')
        if not view.action == 'create':
            return data_to_validate
        title_id = view.kwargs.get('title_id')
        if not title_id:
            raise serializers.ValidationError('Не указано произведение.')
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError('Нет данных запроса.')
        if request.user.reviews.filter(title=title_id).exists():
            raise serializers.ValidationError(
                'Допустим только один обзор на произведение.')
        return data_to_validate


class CommentSerializer(AuthorSerializer):
    """Сериализатор комментариев."""

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
