from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

blog_router = SimpleRouter()
blog_router.register("tipos", TipoViewSet)
blog_router.register("enderecos", EnderecoViewSet)
blog_router.register("contatos", ContatoViewSet)
blog_router.register("empresas", EmpresaViewSet)
blog_router.register("users", UserViewSet)
blog_router.register("setores", SetorViewSet)
blog_router.register("matriculas", MatriculaViewSet)


urlpatterns = [
    path("", include(blog_router.urls)),
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
