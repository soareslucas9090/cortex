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
blog_router.register("setorusers", SetorUserViewSet)
blog_router.register("tiposmatricula", TipoMatriculaViewSet)
blog_router.register("matriculas", MatriculaViewSet)


urlpatterns = [
    path("", include(blog_router.urls)),
]
