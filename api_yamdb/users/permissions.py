from rest_framework.permissions import BasePermission  # type: ignore


class AdminOnlyPermission(BasePermission):
    """Только  для админа."""

    def has_permission(self, request, view):
        """Проверка."""
        if request.method not in ('PUT',):
            return False
        if not request.user.is_authenticated:
            return False
        return request.user.is_admin
