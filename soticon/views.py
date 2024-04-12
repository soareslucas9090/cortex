from datetime import datetime

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from gerUsuarios import models as gerUsuarios

from .models import *
from .serializers import *


class UserSoticonViewSet(ModelViewSet):
    queryset = UserSoticon.objects.all()
    serializer_class = UserSoticonSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        usuario = self.request.query_params.get("usuario", None)

        if usuario:
            queryset = queryset.filter(usuario=usuario)
            return queryset

        return queryset


class StrikeViewSet(ModelViewSet):
    queryset = Strike.objects.all()
    serializer_class = StrikeSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        nome = self.request.query_params.get("nome", None)

        if nome:
            queryset = queryset.filter(user_soticon__usuario__nome=nome)
            return queryset

        return queryset


class JustificativaViewSet(ModelViewSet):
    queryset = Justificativa.objects.all()
    serializer_class = JustificativaSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


class PosicaoFilaViewSet(ModelViewSet):
    queryset = PosicaoFila.objects.all()
    serializer_class = PosicaoFilaSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


class RotaViewSet(ModelViewSet):
    queryset = Rota.objects.all()
    serializer_class = RotaSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.query_params.get("status", None)

        if status:
            queryset = queryset.filter(status=status)
            return queryset

        data = self.request.query_params.get("data")
        format = "%Y-%m-%d"
        data_formatada = None

        try:
            data_formatada = datetime.strptime(data, format)
        except:
            data_formatada = None

        if data_formatada:
            return queryset.filter(data__date=data_formatada.date())

        return queryset
