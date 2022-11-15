from rest_framework import permissions


class IsAuthorsObjectOrSupport(permissions.BasePermission):
    """Allows access only to the author or support."""

    def has_object_permission(self, request, view, obj):
        if obj.user_id == request.user.id or request.user.is_support:
            return bool(True)
