from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

ouvidoria_router = SimpleRouter()
ouvidoria_router.register("statusreclamacoes", StatusReclamacaoViewSet)
ouvidoria_router.register("tiposeclamacoes", TipoReclamacaoViewSet)
ouvidoria_router.register("blocos", BlocoViewSet)
ouvidoria_router.register("reclamacoes", ReclamacaoViewSet)

urlpatterns = [
    path("", include(ouvidoria_router.urls)),
]
