"""Контроллеры."""

from rest_framework import viewsets  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore

from .serializers import UserSerializer
from .permissions import AdminOnlyPermission

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Обработка пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnlyPermission,)
    lookup_field = 'username'
