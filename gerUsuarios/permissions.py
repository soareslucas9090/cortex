from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

from .models import User


class IsAdminOrTI(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        else:
            adminOrTI = ["admin", "ti"]
            return request.user.tipo.nome.lower() in adminOrTI
