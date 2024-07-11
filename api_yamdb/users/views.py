"""Контроллеры."""

from rest_framework import viewsets  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore

from .serializers import UserSerializer
from .permissions import AdminOnlyPermission, AuthenticatedOnlyPermission

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Обработка пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnlyPermission,)
    lookup_field = 'username'


class SingleUserViewSet(viewsets.ModelViewSet):
    """Обработка учётной записи."""

    serializer_class = UserSerializer
    permission_classes = (AuthenticatedOnlyPermission,)

    def get_queryset(self):
        """Получение учётной записи."""
        return User.objects.get_object_or_404(
            username=self.request.user.username)
