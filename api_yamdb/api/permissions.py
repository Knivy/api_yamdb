from rest_framework.permissions import (  # type: ignore
    SAFE_METHODS, BasePermission)
from rest_framework.exceptions import MethodNotAllowed  # type: ignore


class AdminOrReadListOnlyPermission(BasePermission):
    """Только чтение списка или только для админа."""

    def has_permission(self, request, view):
        """Проверка метода."""
        if view.action == 'list':
            return True
        if not request.user.is_authenticated:
            return False
        if request.method in {'POST', 'DELETE'}:
            return request.user.is_admin
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
        if request.method in {'POST', 'PATCH', 'DELETE'}:
            return request.user.is_authenticated and request.user.is_admin
        raise MethodNotAllowed(request.method)


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
                and (request.user.is_admin
                     or request.user == text_object.author
                     or request.user.is_moderator))
