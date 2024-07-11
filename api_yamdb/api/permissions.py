from rest_framework.permissions import (  # type: ignore
    SAFE_METHODS, BasePermission)
from rest_framework.exceptions import MethodNotAllowed  # type: ignore


class AdminOrReadListOnlyPermission(BasePermission):
    """Только чтение списка или только для админа."""

    def has_permission(self, request, view):
        """Проверка метода."""
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.method in ('POST', 'DELETE'):
            return request.user.is_admin
        return False

    def has_object_permission(self, request, view, obj):
        """Запрет просмотра одного объекта не-админу."""
        return request.user.is_admin


class AdminOrReadOnlyPermission(BasePermission):
    """Только чтение или только для админа."""

    def has_permission(self, request, view):
        """Проверка метода."""
        if request.method not in SAFE_METHODS:
            if request.method in ('POST', 'PATCH', 'DELETE'):
                return request.user.is_authenticated and request.user.is_admin
            raise MethodNotAllowed(request.method)
        return True


class TextPermission(BasePermission):
    """Разрешения на доступ к текстам отзывов и комментариев."""

    def has_permission(self, request, view):
        """Проверка метода."""
        if request.method in SAFE_METHODS:
            return True
        if request.method in ('PUT',):
            raise MethodNotAllowed(request.method)
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Доступ к объектам."""
        return (request.user.is_authenticated and
                (request.user.is_admin or request.user == obj.author
                 or request.user.is_moderator))
