from rest_framework.permissions import (  # type: ignore
    SAFE_METHODS, BasePermission, IsAuthenticatedOrReadOnly)
from rest_framework.exceptions import (MethodNotAllowed,  # type: ignore
                                       NotAuthenticated)


class AdminOrReadOnlyPermission(BasePermission):
    """Только чтение или только для админа."""

    def has_permission(self, request, view):
        """Проверка метода."""
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_superuser_or_admin))


class TextPermission(IsAuthenticatedOrReadOnly):
    """Разрешения на доступ к текстам отзывов и комментариев."""

    def has_object_permission(self, request, view, text_object):
        """Доступ к объектам."""
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_moderator_or_higher
                         or request.user == text_object.author)))


class AdminOnlyPermission(BasePermission):
    """Только  для админа."""

    def has_permission(self, request, view):
        """Проверка."""
        return (request.user.is_authenticated
                and request.user.is_superuser_or_admin)


class NotUserModeratorPermission(BasePermission):
    """Особые разрешения для метода PATCH."""

    def has_permission(self, request, view):
        """Проверка."""
        if not request.user.is_authenticated:
            raise NotAuthenticated(request.method)
        if (request.user.is_user
           or request.user.is_moderator):
            return False
        raise MethodNotAllowed(request.method)


class ForbiddenPermission(BasePermission):
    """Запрещен."""

    def has_permission(self, request, view):
        """Проверка."""
        raise MethodNotAllowed(request.method)
