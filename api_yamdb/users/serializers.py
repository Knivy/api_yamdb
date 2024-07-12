"""Сериализаторы."""

import re

from rest_framework import serializers  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore

from .constants import NAME_MAX_LENGTH, EMAIL_MAX_LENGTH

User = get_user_model()


class UsernameEmailValidationSerializer(serializers.Serializer):
    """Сериализатор валидации логина и емайла."""

    class Meta:
        abstract = True

    def validate_username(self, value):
        """Проверка логина."""
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Нельзя назвать логин "me".'
            )
        if len(value) > NAME_MAX_LENGTH:
            raise serializers.ValidationError(
                f'Длина логина не должна превышать '
                f'{NAME_MAX_LENGTH} символов.'
            )
        if not re.fullmatch(r'^[\w\d\.@+-]+$', value):
            raise serializers.ValidationError(
                'Логин содержит недопустимые символы.'
            )
        return value
    
    def validate_email(self, value):
        """Проверка email."""
        if len(value) > EMAIL_MAX_LENGTH:
            raise serializers.ValidationError(
                'Email слишком длинный.'
            )
        return value


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


class UserGetOrCreationSerializer(UsernameEmailValidationSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
