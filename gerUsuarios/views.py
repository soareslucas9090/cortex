from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
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
        AllowAny,
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
        AllowAny,
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
        AllowAny,
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
