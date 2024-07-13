from rest_framework.permissions import (  # type: ignore
    SAFE_METHODS, BasePermission)
from rest_framework.exceptions import MethodNotAllowed  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore


class AdminOrReadListOnlyPermission(BasePermission):
    """Только чтение списка или только для админа."""

    def has_permission(self, request, view):
        """Проверка метода."""
        if view.action == 'list':
            return True
        if not request.user.is_authenticated:
            return False
        if request.method in {'POST', 'DELETE'}:
            return request.user.is_superuser_or_admin
        if (request.method == 'PATCH'
           and (request.user.is_user or request.user.is_moderator)):
            return False
        raise MethodNotAllowed(request.method)


class AdminOrReadOnlyPermission(BasePermission):
    """Только чтение или только для админа."""

    def has_permission(self, request, view):
        """Проверка метода."""
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and request.user.is_superuser_or_admin)


class TextPermission(BasePermission):
    """Разрешения на доступ к текстам отзывов и комментариев."""

    def has_permission(self, request, view):
        """Проверка метода."""
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'PUT':
            raise MethodNotAllowed(request.method)
        return request.user.is_authenticated

    def has_object_permission(self, request, view, text_object):
        """Доступ к объектам."""
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and (request.user.is_moderator_or_higher
                     or request.user == text_object.author))


class AdminOnlyPermission(BasePermission):
    """Только  для админа."""

    def has_permission(self, request, view):
        """Проверка."""
        return (request.user.is_authenticated
                and request.user.is_superuser_or_admin)


class AuthenticatedOnlyPermission(IsAuthenticated):
    """Только  для аутентифицированных."""

    def has_permission(self, request, view):
        """Проверка."""
        if not request.user.is_authenticated:
            return False
        if request.method not in {'POST', 'PATCH', 'GET'}:
            raise MethodNotAllowed(request.method)
        return True
