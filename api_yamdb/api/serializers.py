"""Сериализаторы."""

from rest_framework import serializers  # type: ignore
from rest_framework.relations import SlugRelatedField  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from django.contrib.auth.tokens import default_token_generator  # type: ignore

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import (validate_username as models_validate_username,
                          validate_email as models_validate_email)

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = ('name',
                  'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = ('name',
                  'slug')
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
        allow_empty=False,
    )

    class Meta:
        model = Title
        fields = ('name',
                  'year',
                  'description',
                  'genre',
                  'category')

    def to_representation(self, instance):
        """Представление объекта."""
        return (TitleReadSerializer(self, context=self.context)
                .to_representation(instance))


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор произведений на чтение."""

    category = CategorySerializer()
    genre = GenreSerializer(
        many=True,
    )
    rating = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')


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
        fields = ('id',
                  'text',
                  'author',
                  'score',
                  'pub_date')

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
        fields = ('id',
                  'text',
                  'author',
                  'pub_date')


class UsernameEmailValidationSerializer:
    """Сериализатор валидации логина и емайла."""

    def validate_username(self, username):
        """Проверка логина."""
        return models_validate_username(username)

    def validate_email(self, email):
        """Проверка email."""
        return models_validate_email(email)


class UserSerializer(UsernameEmailValidationSerializer,
                     serializers.ModelSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')
        lookup_field = 'username'


class SingleUserSerializer(UserSerializer):
    """Сериализатор учётной записи."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class UserGetOrCreationSerializer(UsernameEmailValidationSerializer,
                                  serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()

    def validate(self, data_to_validate):
        """Проверка существования пользователя."""
        email = data_to_validate.get('email')
        username = data_to_validate.get('username')
        if (User.objects.filter(email=email)
                        .exclude(username=username).exists()):
            raise serializers.ValidationError('Емайл уже существует.')
        if (User.objects.filter(username=username)
                        .exclude(email=email).exists()):
            raise serializers.ValidationError(
                'Имя пользователя уже существует.')
        return data_to_validate


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data_to_validate):
        """Проверка кода подтверждения."""
        username = data_to_validate.get('username')
        confirmation_code = data_to_validate.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError('Неверный код подтверждения.')
        return data_to_validate
