from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import *
from .serializers import *


class TipoViewSet(ModelViewSet):
    queryset = models.Tipo.objects.all()
    serializer_class = serializers.TipoSerializer
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
    queryset = models.Endereco.objects.all()
    serializer_class = serializers.EnderecoSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


class ContatoViewSet(ModelViewSet):
    queryset = models.Contato.objects.all()
    serializer_class = serializers.ContatoSerializer
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
    queryset = models.Empresa.objects.all()
    serializer_class = serializers.EmpresaSerializer
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


class UsuarioViewSet(ModelViewSet):
    queryset = models.Usuario.objects.all()
    serializer_class = serializers.UsuarioSerializer
    permission_classes = [
        IsAuthenticated,
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

    @action(detail=True, methods=["get"])
    def matricula(self, request, pk=None):
        # A paginação não afeta métodos feitos por nós na ViewSet, por isso precisamos criar uma paginação específica
        self.pagination_class.page_size = 3
        matricula = models.MATRICULA.objects.filter(ID_USUARIO=pk)
        page = self.paginate_queryset(matricula)

        if page is not None:
            serializer = serializers.MatriculaSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.MatriculaSerializer(
            matricula.MATRICULA_ID_USUARIO.all(), many=True
        )
        return Response(serializer.data)


"""
Método de validação de login usado antes da decisão de usar functions
class UsuarioSenhaViewSet(ModelViewSet):
    queryset = models.USUARIO.objects.all()
    serializer_class = serializers.UsuarioSenhaSerializer

    def get_queryset(self):
        queryset = self.queryset
        nome = self.request.query_params.get('nome', None)
        senha = self.request.query_params.get('senha', None)
        
        if nome is not None:
            queryset = queryset.filter(NOME=nome)
        
        if senha is not None:
            queryset = queryset.filter(SENHA=senha)
            
        return queryset
"""


class SetorViewSet(ModelViewSet):
    queryset = models.SETOR.objects.all()
    serializer_class = serializers.SetorSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


class SetorUsuarioViewSet(ModelViewSet):
    queryset = models.SETOR_USUARIO.objects.all()
    serializer_class = serializers.SetorUsuarioSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


class AlteracaoUsuarioViewSet(ModelViewSet):
    queryset = models.ALTERACAO_USUARIO.objects.all()
    serializer_class = serializers.AlteracaoUsuarioSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


class TipoMatriculaViewSet(ModelViewSet):
    queryset = models.TIPO_MATRICULA.objects.all()
    serializer_class = serializers.TipoMatriculaSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


class MatriculaViewSet(ModelViewSet):
    queryset = models.MATRICULA.objects.all()
    serializer_class = serializers.MatriculaSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


class PermissoesViewSet(ModelViewSet):
    queryset = models.PERMISSOES.objects.all()
    serializer_class = serializers.PermissoesSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]
