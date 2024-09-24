from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

from gerUsuarios.models import Setor_User


class IsSectorAuthorized(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        else:
            adminOrTI = ["admin", "ti"]
            if request.user.tipo.nome.lower() in adminOrTI:
                return True

            setoresAutorizados = [
                "direcao geral",
                "direcao de ensino",
                "direcao de administracao e planejamento",
                "ti",
            ]

            for setor in request.user.setores.all():
                if str(setor) in setoresAutorizados:
                    return True
            return False
