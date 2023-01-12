from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """Устаналвивает разрешение для автора или админа."""

    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id or request.user.is_staff:
            return bool(True)


class IsAdminOrSupport(permissions.BasePermission):
    """Устанавливает разрешение для агента поддержки или админа."""

    def has_permission(self, request, view):
        return bool(request.user.is_staff or request.user.is_support)


class IsAdmin(permissions.BasePermission):
    """Устанавливает разрешение для администратора."""

    def has_permission(self, request, view):
        return bool(request.user.is_staff)
