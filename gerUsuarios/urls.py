from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

gerUsers_router = SimpleRouter()
gerUsers_router.register("tipos", TipoViewSet)
gerUsers_router.register("enderecos", EnderecoViewSet)
gerUsers_router.register("contatos", ContatoViewSet)
gerUsers_router.register("empresas", EmpresaViewSet)
gerUsers_router.register("users", UserViewSet)
gerUsers_router.register("setores", SetorViewSet)
gerUsers_router.register("matriculas", MatriculaViewSet)
gerUsers_router.register("deficiencias", DeficienciaViewSet)


urlpatterns = [
    path("", include(gerUsers_router.urls)),
    path(
        "password/reset/", PasswordResetRequestAPIView.as_view(), name="reset-password"
    ),
    path(
        "password/reset/code",
        PasswordResetCodeConfirmAPIView.as_view(),
        name="confirm-code",
    ),
    path(
        "password/reset/confirm",
        PasswordResetConfirmAPIView.as_view(),
        name="confirm-password",
    ),
    path(
        "users/inserir_dados_completos/alunos/",
        InserirVariosAlunosCompletosView.as_view(),
        name="insert-multiple-students",
    ),
    path(
        "users/inserir_dados_completos/usuarios/",
        InserirVariosUsuariosCompletosView.as_view(),
        name="insert-multiple-users",
    ),
]
