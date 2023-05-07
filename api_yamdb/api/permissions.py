"""Permissions access."""

from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminReadOnly(BasePermission):
    """Admin or read."""

    def has_permission(self, request, view):
        """GET."""
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


class Admin(BasePermission):
    """Admin."""

    def has_permission(self, request, view):
        """GET."""
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class AdminModerAuthorReadOnly(BasePermission):
    """Admin / Moder/ Author/ Read."""

    def has_permission(self, request, view):
        """GET."""
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """GET, PUT, DELETE."""
        return request.method in SAFE_METHODS or (
            obj.author == request.user
            or (
                request.user.is_authenticated
                and (
                    request.user.is_moderator
                    or request.user.is_admin
                    or request.user.is_superuser
                )
            )
        )
