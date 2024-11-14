from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import *
from .serializers import *


@extend_schema(tags=["Watt.Watt"])
class LeituraViewSet(ModelViewSet):
    queryset = Leitura.objects.all()
    serializer_class = LeituraSerializer
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


from django.http import JsonResponse


def consumo_atual(request):
    # Pega o último valor de leitura
    try:
        leitura = Leitura.objects.latest("created_at")  # Última leitura registrada
        print(leitura)
        potencia = leitura.potencia  # Potência em watts

        # Cálculo do consumo (em kWh)
        consumo = 0.853 * (potencia / 1000)  # Consumo em kWh

        # Retorna o consumo atual em formato JSON (para a requisição JavaScript)
        return JsonResponse({"consumo": round(consumo, 2)})
    except Exception as e:
        print(e)
        return JsonResponse({"error": "Erro ao obter o consumo atual"})


def exibir_consumo(request):
    try:
        # Renderiza o template consumo.html
        return render(request, "home.html")
    except Exception as e:
        print(e)
