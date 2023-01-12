from rest_framework import permissions


class IsAuthorsObjectOrSupport(permissions.BasePermission):
    """Устанавливает разрешение для автора обращения или агента поддержки."""

    def has_object_permission(self, request, view, obj):
        # obj - instance model Ticket
        if obj.user_id == request.user.id or request.user.is_support:
            return bool(True)

class TicketNotFrozenAndClosed(permissions.BasePermission):
    """Устанавливает разрешение для открытого или не замороженного обращения."""
    # Обращение не должно быть закрыто или заморожено агентом поддержки или админом.

    def has_object_permission(self, request, view, obj):
        # obj - instance model Ticket
        if not obj.frozen and not obj.frozen:
            return bool(True)


class IsOwner(permissions.BasePermission):
    """Устанавливает разрешение только для автора."""

    def has_object_permission(self, request, view, obj):
        # obj - instance model Ticket
        return bool(obj.user_id == request.user.id)

class IsSupport(permissions.BasePermission):
    """Устанавливает разрешение только для агента поддержки."""

    def has_permission(self, request, view):
        return bool(request.user.is_support)
