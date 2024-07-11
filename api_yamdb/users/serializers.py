"""Сериализаторы."""

import re

from rest_framework import serializers  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from rest_framework.validators import UniqueValidator  # type: ignore

from .constants import NAME_MAX_LENGTH, EMAIL_MAX_LENGTH

User = get_user_model()


class ValidationErrorSerializer(serializers.Serializer):
    """Сериализатор ошибок валидации."""

    class Meta:
        abstract = True

    def validate_username(self, value):
        """Проверка логина."""
        if not value:
            raise serializers.ValidationError(
                'Логин не может быть пустым.'
            )
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Нельзя назвать логин "me".'
            )
        if len(value) > NAME_MAX_LENGTH:
            raise serializers.ValidationError(
                f'Длина логина не должна превышать '
                f'{NAME_MAX_LENGTH} символов.'
            )
        if not re.fullmatch(r'^[\w.@+-]+\Z$', value):  # r'^[\w\d\.@+-]+$'
            raise serializers.ValidationError(
                'Логин содержит недопустимые символы.'
            )
        return value
    
    def validate_first_name(self, value):
        """Проверка имени."""
        if len(value) > NAME_MAX_LENGTH:
            raise serializers.ValidationError(
                f'Длина имени не должна превышать {NAME_MAX_LENGTH} '
                f'символов.'
            )
        return value
    
    def validate_last_name(self, value):
        """Проверка фамилии."""
        if len(value) > NAME_MAX_LENGTH:
            raise serializers.ValidationError(
                f'Длина фамилии не должна превышать {NAME_MAX_LENGTH} '
                f'символов.'
            )
        return value
    
    def validate_email(self, value):
        """Проверка email."""
        if not value:
            raise serializers.ValidationError(
                'Email не может быть пустым.'
            )
        if len(value) > EMAIL_MAX_LENGTH:
            raise serializers.ValidationError(
                'Email слишком длинный.'
            )
        return value


class UserSerializer(ValidationErrorSerializer, serializers.ModelSerializer):
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


class UserCreationSerializer(ValidationErrorSerializer,
                             serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
