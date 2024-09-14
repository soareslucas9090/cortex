import random
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from django.core.mail import EmailMultiAlternatives
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import *
from .permissions import *
from .serializers import *


@extend_schema(tags=["Gerenciamento De Usuários.Tipos"])
class TipoViewSet(ModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "post"]

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
        if self.request.method in ["POST", "PATCH"]:
            return [IsAdminOrTI()]

        return super().get_permissions()


@extend_schema(tags=["Gerenciamento De Usuários.Enderecos"])
class EnderecoViewSet(ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        if not IsAdminOrTI().has_permission(self.request, self):
            queryset = queryset.filter(id=self.request.user.contato.endereco.id)

        return queryset

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminOrTI()]

        return super().get_permissions()


@extend_schema(tags=["Gerenciamento De Usuários.Contatos"])
class ContatoViewSet(ModelViewSet):
    queryset = Contato.objects.all()
    serializer_class = ContatoSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        if not IsAdminOrTI().has_permission(self.request, self):
            return queryset.filter(id=self.request.user.contato.id)

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


@extend_schema(tags=["Gerenciamento De Usuários.Empresas"])
class EmpresaViewSet(ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        if not IsAdminOrTI().has_permission(self.request, self):
            return queryset.filter(id=self.request.user.empresa.id)

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


@extend_schema(tags=["Gerenciamento De Usuários.Usuários"])
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        if not IsAdminOrTI().has_permission(self.request, self):
            return queryset.filter(id=self.request.user.id)

        nome = self.request.query_params.get("nome", None)

        if nome:
            queryset = queryset.filter(nome__icontains=nome.lower())

        cpf = self.request.query_params.get("cpf", None)

        if cpf and cpf.isnumeric():
            queryset = queryset.filter(cpf__icontains=cpf)

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
        if self.request.method in ["PATCH", "DELETE", "POST"]:
            return [IsAdminOrTI()]

        return super().get_permissions()


@extend_schema(tags=["Gerenciamento De Usuários.Solicitar Reset de Senha"])
class PasswordResetRequestAPIView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    http_method_names = ["post"]
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Email enviado com sucesso."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="Usuário não possue email cadastrado."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Usuário não encontrado."
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="Erro interno."
            ),
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = serializer.validated_data

        try:
            user = User.objects.get(cpf=serializer["cpf"])
        except:
            return Response(
                {"Não existe usuário com este CPF."}, status=status.HTTP_404_NOT_FOUND
            )

        if "invalidemail.com" in user.email:
            return Response(
                {
                    "O usuário não possui email cadastrado. Por favor, entre em contato com o TI."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        random_code = random.randrange(1000, 9999)
        expiration_time = timezone.now() + timedelta(minutes=15)

        try:
            old_code = PasswordResetCode.objects.get(user=user)
            old_code.delete()
        except:
            pass

        code = PasswordResetCode.objects.create(
            user=user,
            expiration_time=expiration_time,
            code=random_code,
        )

        first_html = """
        <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Código P/ Nova Senha</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #f4f4f4;
                    }
                    .email-container {
                        background-color: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                        border: 1px solid #e0e0e0;
                        max-width: 600px;
                        margin: 40px auto;
                    }
                    h2 {
                        text-align: center;
                        color: #333;
                    }
                    .code-container {
                        background-color: #4CAF50;
                        color: white;
                        font-size: 24px;
                        font-weight: bold;
                        text-align: center;
                        padding: 15px;
                        border-radius: 8px;
                        margin: 20px auto;
                        max-width: 150px;
                    }
                    .footer {
                        text-align: center;
                        margin-top: 20px;
                        font-size: 14px;
                        color: #666;
                    }
                    .footer a {
                        color: #4CAF50;
                        text-decoration: none;
                    }
                </style>
            </head>
            <body>
                <div class="email-container">
                    <h2>Reset de Senha</h2>
                    <p>Olá,</p>
                    <p>Recebemos uma solicitação para redefinir a senha da sua conta. Por favor, use o código abaixo na tela de reset de senha para concluir o processo:</p>
                    
                    <div class="code-container">
        """

        second_html = f"""
                    {code.code}
                    </div>
                    
                    <p>Se você não solicitou uma redefinição de senha, por favor, ignore este email ou entre em contato com o suporte.</p>
                    
                    <div class="footer">
                        IFPI - Campus Floriano - Cortex<br>
                    </div>
                </div>
            </body>
        </html>
        """

        final_html = first_html
        final_html += second_html

        # Crie a instância do email usando EmailMultiAlternatives
        email = EmailMultiAlternatives(
            "Recuperação de senha",
            f"Código de recuperação de senha: {code.code}",  # Texto simples alternativo
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )

        email.attach_alternative(final_html, "text/html")  # Corpo em HTML

        try:
            email.send()
            return Response(
                {"success": "E-mail com o código enviado com sucesso!"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": "Erro ao enviar o e-mail"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema(tags=["Gerenciamento De Usuários.Confirmar Codigo Reset de Senha"])
class PasswordResetCodeConfirmAPIView(GenericAPIView):
    serializer_class = PasswordResetCodeConfirmSerializer
    http_method_names = ["post"]
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(description="Código Válido."),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="Código expirado."),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Usuário não encontrado."
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="Erro interno."
            ),
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = serializer.validated_data

        try:
            user = User.objects.get(cpf=serializer["cpf"])
        except:
            return Response(
                {"error": "Não existe usuário com este CPF."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            valid_code = PasswordResetCode.objects.get(
                user=user, code=serializer["code"]
            )
        except:
            return Response(
                {"error": "Este código não existe."}, status=status.HTTP_400_BAD_REQUEST
            )

        if valid_code.is_expired():
            valid_code.delete()
            return Response(
                {"error": "Este código expirou."}, status=status.HTTP_403_FORBIDDEN
            )

        valid_code.validated = True
        valid_code.save()

        return Response({"success": "Código válido."}, status=status.HTTP_200_OK)


@extend_schema(tags=["Gerenciamento De Usuários.Confirmar Reset de Senha"])
class PasswordResetConfirmAPIView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    http_method_names = ["post"]
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(description="Reset feito."),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Senhas não conferem"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Usuário não encontrado."
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="Erro interno."
            ),
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = serializer.validated_data

        try:
            user = User.objects.get(cpf=serializer["cpf"])
        except:
            return Response(
                {"error": "Não existe usuário com este CPF."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            valid_code = PasswordResetCode.objects.get(user=user, validated=True)
        except:
            return Response(
                {"error": "Não há código de reset de senha válido para o usuário."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer["password"] != serializer["password_confirm"]:
            return Response(
                {"error": "Senhas não conferem."}, status=status.HTTP_400_BAD_REQUEST
            )

        nova_senha = make_password(serializer["password"])

        user.password = nova_senha

        user.save()

        valid_code.delete()

        return Response({"success": "Senha atualizada."}, status=status.HTTP_200_OK)


@extend_schema(tags=["Gerenciamento De Usuários.Inserir Vários Alunos"])
class InserirVariosAlunosCompletosView(GenericAPIView):
    serializer_class = InserirVariosAlunosCompletosWrapperSerializer
    http_method_names = ["post"]
    permission_classes = [IsAdminOrTI]

    @extend_schema(
        examples=[
            OpenApiExample(
                "Exemplo de Inserção de Aluno",
                value=[
                    {
                        "endereco": {
                            "logradouro": "(Obrigatório) Rua Exemplo",
                            "cidade": "(Obrigatório) Exemplo City",
                            "estado": "(Obrigatório) PI",
                            "bairro": "(Obrigatório) Bairro Exemplo",
                            "cep": "(Opcional) 64800000",
                            "complemento": "(Opcional) P4, APT5",
                            "num_casa": 123,
                        },
                        "email_externo": "emailPessoal@gmail.com",
                        "tel": "11999999999",
                        "cpf": "12345678900",
                        "nome": "João Exemplo",
                        "data_nascimento": "1990-12-30",
                        "matricula": "202312345",
                        "validade_matricula": "2025-01-01",
                        "expedicao_matricula": "2023-01-01",
                    }
                ],
            )
        ],
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(description="Usários criados."),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Dados errados."),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Não autorizado."
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="Erro interno."
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)

        # Valida os dados
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Usuários criados com sucesso!"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Gerenciamento De Usuários.Inserir Vários Usuários"])
class InserirVariosUsuariosCompletosView(GenericAPIView):
    serializer_class = InserirVariosUsuariosCompletosWrapperSerializer
    http_method_names = ["post"]
    permission_classes = [AllowAny]

    @extend_schema(
        examples=[
            OpenApiExample(
                "Exemplo de Inserção de Aluno",
                value=[
                    {
                        "endereco": {
                            "logradouro": "(Obrigatório) Rua Exemplo",
                            "cidade": "(Obrigatório) Exemplo City",
                            "estado": "(Obrigatório) PI",
                            "bairro": "(Obrigatório) Bairro Exemplo",
                            "cep": "(Opcional) 64800000",
                            "complemento": "(Opcional) P4, APT5",
                            "num_casa(Opcional)": 123,
                        },
                        "email_externo": "emailPessoal@gmail.com",
                        "email_institucional": "emailInterno@ifpi.edu.br",
                        "tel": "11999999999",
                        "cpf": "12345678900",
                        "nome": "João Exemplo",
                        "cnpj_empresa": "12345678901234",
                        "tipo": "professor",
                        "setores": ["Coordenacao Informatica", "Coordenacao TADS"],
                        "data_nascimento": "1990-12-30",
                        "matricula": "202312345",
                        "validade_matricula": "2025-01-01",
                        "expedicao_matricula": "2023-01-01",
                    }
                ],
            )
        ],
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(description="Usários criados."),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Dados errados."),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Não autorizado."
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="Erro interno."
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)

        # Valida os dados
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Usuários criados com sucesso!"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Gerenciamento De Usuários.Setores"])
class SetorViewSet(ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "post"]

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


@extend_schema(tags=["Gerenciamento De Usuários.Matriculas"])
class MatriculaViewSet(ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        if not IsAdminOrTI().has_permission(self.request, self):
            return queryset.filter(user=self.request.user)

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

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE", "POST"]:
            return [IsAdminOrTI()]

        return super().get_permissions()
