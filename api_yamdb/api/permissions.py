from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class AdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == User.ADMIN or request.user.is_superuser)
        )


class AdminOrReadOnlyPermission(AdminOnlyPermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )


class AuthorAdminModeratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.role in (User.ADMIN, User.MODERATOR)
            )
        )
