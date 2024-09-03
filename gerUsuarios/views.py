from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import *
from .permissions import *
from .serializers import *


@extend_schema(tags=["GerenciamentoDeUsuários.Tipos"])
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="tipo",
                type=OpenApiTypes.STR,
                description="Filtrar pelo nome do tipo",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method in ["POST", "PATCH", "DELETE"]:
            return [IsAdminOrTI()]

        return super().get_permissions()


@extend_schema(tags=["GerenciamentoDeUsuários.Enderecos"])
class EnderecoViewSet(ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminOrTI()]

        return super().get_permissions()


@extend_schema(tags=["GerenciamentoDeUsuários.Contatos"])
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

        tel = self.request.query_params.get("tel", None)

        if tel and tel.isnumeric():
            queryset = queryset.filter(tel=tel)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="email",
                type=OpenApiTypes.STR,
                description="Filtrar pelo email do contato",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="tel",
                type=OpenApiTypes.STR,
                description="Filtrar pelo telefone do contato",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminOrTI()]

        return super().get_permissions()


@extend_schema(tags=["GerenciamentoDeUsuários.Empresas"])
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

        cnpj = self.request.query_params.get("cnpj", None)

        if cnpj and cnpj.isnumeric():
            queryset = queryset.filter(cnpj=cnpj)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="nome",
                type=OpenApiTypes.STR,
                description="Filtrar pelo nome da empresa",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="cnpj",
                type=OpenApiTypes.STR,
                description="Filtrar pelo CNPJ da empresa",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminOrTI()]

        return super().get_permissions()


@extend_schema(tags=["GerenciamentoDeUsuários.Usuários"])
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        nome = self.request.query_params.get("nome", None)

        if nome:
            queryset = queryset.filter(nome__iexact=nome.lower())

        cpf = self.request.query_params.get("cpf", None)

        if cpf and cpf.isnumeric():
            queryset = queryset.filter(cpf=cpf)

        return queryset

    def create(self, request, *args, **kwargs):
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="nome",
                type=OpenApiTypes.STR,
                description="Filtrar pelo nome do usuario",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="cpf",
                type=OpenApiTypes.STR,
                description="Filtrar pelo CPF do usuário",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminOrTI()]

        return super().get_permissions()


@extend_schema(tags=["GerenciamentoDeUsuários.Setores"])
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="nome",
                type=OpenApiTypes.STR,
                description="Filtrar pelo nome do setor",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminOrTI()]

        return super().get_permissions()


class SetorUserViewSet(ModelViewSet):
    queryset = Setor_User.objects.all()
    serializer_class = Setor_UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_permissions(self):
        if self.request.method in ["POST", "PATCH", "DELETE"]:
            return [IsAdminOrTI()]

        return super().get_permissions()


@extend_schema(tags=["GerenciamentoDeUsuários.Matriculas"])
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="user",
                type=OpenApiTypes.INT,
                description="Filtrar pelo id do usuario",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="user",
                type=OpenApiTypes.INT,
                description="Filtrar a matricula do usuario",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
