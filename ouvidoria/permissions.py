from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print()
        if isinstance(request.user, AnonymousUser):
            return False
        return (
            request.user.tipo.id == 1
            or request.user.tipo.id == 6
            or request.user.tipo.id == 7
        )
