from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import *
from .serializers import *


class StatusReclamacaoViewSet(ModelViewSet):
    queryset = Leitura.objects.all()
    serializer_class = LeituraSerializer
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]
