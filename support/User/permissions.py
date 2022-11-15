from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """Allows access only to the author or administrator."""

    def has_object_permission(self, request, view, obj):
        print(obj)
        if obj.id == request.user.id or request.user.is_staff:
            return bool(True)


class IsAdminOrSupport(permissions.BasePermission):
    """Allows access only to the administrator or support staff member."""

    def has_permission(self, request, view):
        return bool(request.user.is_staff or request.user.is_support)


class IsAdmin(permissions.BasePermission):
    """Allows access only to the administrator."""

    def has_permission(self, request, view):
        return bool(request.user.is_staff)
