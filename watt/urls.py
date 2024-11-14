from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

watt_router = SimpleRouter()
watt_router.register("leituras", LeituraViewSet)


urlpatterns = [
    path("", include(watt_router.urls)),
    path("consumo/", consumo_atual, name="consumo_atual"),
    path("exibir-consumo/", exibir_consumo, name="exibir_consumo"),
]
