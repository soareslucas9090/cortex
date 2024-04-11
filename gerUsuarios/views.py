from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import *
from .serializers import *


class TipoViewSet(ModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        tipo = self.request.query_params.get("tipo", None)

        if tipo:
            queryset = queryset.filter(nome=tipo)

            return queryset

        return queryset


class EnderecoViewSet(ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


class ContatoViewSet(ModelViewSet):
    queryset = Contato.objects.all()
    serializer_class = ContatoSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        email = self.request.query_params.get("email", None)

        if email:
            queryset = queryset.filter(email=email)
            return queryset

        tel = self.request.query_params.get("tel", None)

        if tel and tel.isnumeric():
            queryset = queryset.filter(tel=tel)
            return queryset

        return queryset


class EmpresaViewSet(ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        nome = self.request.query_params.get("nome", None)

        if nome:
            queryset = queryset.filter(nome=nome)
            return queryset

        cnpj = self.request.query_params.get("cnpj", None)

        if cnpj and cnpj.isnumeric():
            queryset = queryset.filter(cnpj=cnpj)
            return queryset

        return queryset


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def create(self, request, *args, **kwargs):
        if "date_joined" in request.data:
            request.data.pop("date_joined")
        if "is_superuser" in request.data:
            request.data.pop("is_superuser")
        if "is_staff" in request.data:
            request.data.pop("is_staff")
        if "is_admin" in request.data:
            request.data.pop("is_admin")
        if "is_ativo" in request.data:
            request.data.pop("is_active")
        if "last_login" in request.data:
            request.data.pop("last_login")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password256 = make_password(password=request.data["password"])

        serializer.save(password=password256)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        if "date_joined" in request.data:
            request.data.pop("date_joined")
        if "is_superuser" in request.data:
            request.data.pop("is_superuser")
        if "is_staff" in request.data:
            request.data.pop("is_staff")
        if "is_admin" in request.data:
            request.data.pop("is_admin")
        if "is_active" in request.data:
            request.data.pop("is_active")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()

        nome = self.request.query_params.get("nome", None)

        if nome:
            queryset = queryset.filter(nome=nome)
            return queryset

        cpf = self.request.query_params.get("cpf", None)

        if cpf and cpf.isnumeric():
            queryset = queryset.filter(cpf=cpf)
            return queryset

        return queryset


class SetorViewSet(ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        nome = self.request.query_params.get("nome", None)

        if nome:
            queryset = queryset.filter(nome=nome)
            return queryset

        return queryset


class SetorUserViewSet(ModelViewSet):
    queryset = Setor_User.objects.all()
    serializer_class = Setor_UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


"""
class AlteracaoUsuarioViewSet(ModelViewSet):
    queryset = ALTERACAO_USUARIO.objects.all()
    serializer_class = AlteracaoUsuarioSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]
"""


class TipoMatriculaViewSet(ModelViewSet):
    queryset = Tipo_Matricula.objects.all()
    serializer_class = Tipo_MatriculaSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        descricao = self.request.query_params.get("descricao", None)

        if descricao:
            queryset = queryset.filter(descricao=descricao)
            return queryset

        return queryset


class MatriculaViewSet(ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.query_params.get("user", None)

        if user and user.isnumeric():
            queryset = queryset.filter(user=user)
            return queryset

        tipo_matricula = self.request.query_params.get("tipo", None)

        if tipo_matricula and tipo_matricula.isnumeric():
            queryset = queryset.filter(tipo_matricula=tipo_matricula)
            return queryset

        matricula = self.request.query_params.get("matricula", None)

        if matricula:
            queryset = queryset.filter(matricula=matricula)
            return queryset

        return queryset
