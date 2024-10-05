from rest_framework.permissions import SAFE_METHODS, BasePermission


class MyBasePermission(BasePermission):
    """Базовый кастомный пермишн."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated


class OwnerOrReadOnly(MyBasePermission):
    """
    Права доступа на изменение только для владельцем котика,
    для других только чтение.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user == obj.owner


class AuthorOrReadOnly(MyBasePermission):
    """
    Права доступа на изменение рейтинга котика
    только пользователям, который оценил, для других только чтение.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user == obj.user


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_staff
        )
