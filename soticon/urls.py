from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

soticon_router = SimpleRouter()
soticon_router.register("users", UserSoticonViewSet)
soticon_router.register("strikes", StrikeViewSet)
soticon_router.register("justificativas", JustificativaViewSet)
soticon_router.register("posicoes", PosicaoFilaViewSet)
soticon_router.register("rotas", RotaViewSet)
soticon_router.register("tickets", TicketsViewSet)
soticon_router.register("reservar_ticket", ReservarTickets, basename="reservar_ticket")
soticon_router.register(
    "verificar_tickets", VerificarTickets, basename="verificar_tickets"
)
soticon_router.register("finalizar_rota", FinalizarRota, basename="finalizar_rota")

urlpatterns = [
    path("", include(soticon_router.urls)),
]
