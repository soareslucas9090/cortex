from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

from gerUsuarios.models import Setor_User


class IsSectorAuthorizedToChangeRoutes(permissions.BasePermission):
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


class IsAuthorizedToOperateRoutes(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False

        tiposAutorizados = [
            "admin",
            "ti",
            "motorista",
            "diretor.geral",
            "diretor.ensino",
        ]
        if request.user.tipo.nome.lower() in tiposAutorizados:
            return True

        setoresAutorizados = ["guarita"]

        for setor in request.user.setores.all():
            if str(setor) in setoresAutorizados:
                return True

        return False


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False

        if request.user.tipo.nome.lower() == "aluno":
            return True

        return False
