from rest_framework.permissions import BasePermission  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework.exceptions import MethodNotAllowed  # type: ignore


class AdminOnlyPermission(BasePermission):
    """Только  для админа."""

    def has_permission(self, request, view):
        """Проверка."""
        if request.method not in ('PUT',):
            return False
        if not request.user.is_authenticated:
            return False
        return request.user.is_admin


class AuthenticatedOnlyPermission(IsAuthenticated):
    """Только  для аутентифицированных."""

    def has_permission(self, request, view):
        """Проверка."""
        if not request.user.is_authenticated:
            return False
        if request.method not in ('GET', 'PATCH'):
            raise MethodNotAllowed(request.method)
        return True
