from datetime import date, datetime, timedelta

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import *
from .permissions import *
from .serializers import *


class StatusReclamacaoViewSet(ModelViewSet):
    queryset = StatusReclamacao.objects.all()
    serializer_class = StatusReclamacaoSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        descricao = self.request.query_params.get("descricao", None)
        if status:
            queryset = queryset.filter(descricao=descricao)

        isativo = self.request.query_params.get("isativo", None)
        if isativo:
            if isativo.lower() == "false":
                isativo = False
                return queryset.filter(isativo=isativo)

            elif isativo.lower() == "true":
                isativo = True
                return queryset.filter(isativo=isativo)

        return queryset.filter(isativo=isativo)

    def get_permissions(self):
        if self.request.method in ["POST", "PATCH", "DELETE"]:
            return [
                IsAdminUser(),
            ]
        return super().get_permissions()


class TipoReclamacaoViewSet(ModelViewSet):
    queryset = TipoReclamacao.objects.all()
    serializer_class = TipoReclamacaoSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        descricao = self.request.query_params.get("descricao", None)
        if status:
            queryset = queryset.filter(descricao=descricao)

        isativo = self.request.query_params.get("isativo", None)
        if isativo:
            if isativo.lower() == "false":
                isativo = False
                return queryset.filter(isativo=isativo)

            elif isativo.lower() == "true":
                isativo = True
                return queryset.filter(isativo=isativo)

        return queryset.filter(isativo=isativo)

    def get_permissions(self):
        if self.request.method in ["POST", "PATCH", "DELETE"]:
            return [
                IsAdminUser(),
            ]
        return super().get_permissions()


class BlocoViewSet(ModelViewSet):
    queryset = Bloco.objects.all()
    serializer_class = BlocoSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        descricao = self.request.query_params.get("descricao", None)
        if status:
            queryset = queryset.filter(descricao=descricao)

        isativo = self.request.query_params.get("isativo", None)
        if isativo:
            if isativo.lower() == "false":
                isativo = False
                return queryset.filter(isativo=isativo)

            elif isativo.lower() == "true":
                isativo = True
                return queryset.filter(isativo=isativo)

        return queryset.filter(isativo=isativo)

    def get_permissions(self):
        if self.request.method in ["POST", "PATCH", "DELETE"]:
            return [
                IsAdminUser(),
            ]
        return super().get_permissions()


class ReclamacaoViewSet(ModelViewSet):
    queryset = Reclamacao.objects.all()
    serializer_class = ReclamacaoSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        data = self.request.query_params.get("data")
        data_formatada = None

        try:
            data_formatada = datetime.strptime(data, format)
        except:
            data_formatada = None

        if data_formatada:
            queryset.filter(data_reclamacao=data_formatada)

        status_reclamacao_id = self.request.query_params.get("status_reclamacao_id")

        status_reclamacao = StatusReclamacao.objects.get(pk=status_reclamacao_id)

        if status_reclamacao:
            queryset = queryset.filter(status_reclamacao=status_reclamacao)

        tipo_reclamacao_id = self.request.query_params.get("tipo_reclamacao_id")

        tipo_reclamacao = TipoReclamacao.objects.get(pk=tipo_reclamacao_id)

        if tipo_reclamacao:
            queryset = queryset.filter(tipo_reclamacao=tipo_reclamacao)

        bloco_id = self.request.query_params.get("bloco_id")

        bloco = TipoReclamacao.objects.get(pk=bloco_id)

        if bloco:
            queryset = queryset.filter(bloco=bloco)

        lida = self.request.query_params.get("lida", None)
        if lida:
            if lida.lower() == "false":
                lida = False
                queryset.filter(lida=lida)

            elif lida.lower() == "true":
                lida = True
                queryset.filter(lida=lida)

        return queryset

    def get_permissions(self):
        if self.request.method in ["PATCH"]:
            return [
                IsAdminUser(),
            ]
        return super().get_permissions()
