from rest_framework.permissions import SAFE_METHODS, BasePermission


class OwnerOrReadOnly(BasePermission):
    """
    Права доступа на изменение только для владельца котика,
    для других только чтение.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user == obj.owner


# TODO Дублирование пермишенов
class AuthorOrReadOnly(BasePermission):
    """
    Права доступа на изменение только для владельца котика,
    для других только чтение.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user == obj.user


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_staff
        )
