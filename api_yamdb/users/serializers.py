"""Сериализаторы."""

import re

from rest_framework import serializers  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from rest_framework.validators import UniqueValidator  # type: ignore

from .constants import NAME_MAX_LENGTH

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
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


class UserCreationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_username(self, value):
        """Проверка имени пользователя."""
        if not value:
            raise serializers.ValidationError(
                'Имя пользователя не может быть пустым.'
            )
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Нельзя назвать пользователя "me".'
            )
        if len(value) > NAME_MAX_LENGTH:
            raise serializers.ValidationError(
                f'Длина имени пользователя не должна превышать '
                f'{NAME_MAX_LENGTH} символов.'
            )
        if not re.fullmatch(r'^[\w\d\.@+-]+$', value):
            raise serializers.ValidationError(
                'Имя пользователя содержит недопустимые символы.'
            )
        return value


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
