"""Сериализаторы."""

from rest_framework import serializers  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')
        lookup_field = 'username'
