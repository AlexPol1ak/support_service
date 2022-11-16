from rest_framework import permissions


class IsAuthorsObjectOrSupport(permissions.BasePermission):
    """Allows access only to the author or support."""

    def has_object_permission(self, request, view, obj):
        # obj - instance model Ticket
        if obj.user_id == request.user.id or request.user.is_support:
            return bool(True)

class TicketNotFrozenAndClosed(permissions.BasePermission):
    """Provides access if the ticket is not frozen and closed."""

    def has_object_permission(self, request, view, obj):
        # obj - instance model Ticket
        if not obj.frozen and not obj.frozen:
            return bool(True)


class IsOwner(permissions.BasePermission):
    """Provides access to the author"""

    def has_object_permission(self, request, view, obj):
        # obj - instance model Ticket
        return bool(obj.user_id == request.user.id)
