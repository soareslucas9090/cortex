from datetime import date, datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import *
from .serializers import *


class UserSoticonViewSet(ModelViewSet):
    queryset = UserSoticon.objects.all()
    serializer_class = UserSoticonSerializer
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        usuario = self.request.query_params.get("usuario", None)

        if usuario:
            queryset = queryset.filter(usuario=usuario)
            return queryset

        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data_atual = date.today()
        ticket_reservado = Tickets.objects.filter(
            Q(user_soticon=instance, reservado=True) & Q(rota__data=data_atual)
        ).first()

        if ticket_reservado:
            serializer_data = serializer.data
            serializer_data["ticket_reservado"] = (
                ticket_reservado.posicao_fila.num_ticket
            )
            return Response(serializer_data)
        else:
            return Response(serializer.data)


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
        AllowAny,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


class PosicaoFilaViewSet(ModelViewSet):
    queryset = PosicaoFila.objects.all()
    serializer_class = PosicaoFilaSerializer
    permission_classes = [
        AllowAny,
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


class TicketsViewSet(ModelViewSet):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


class ReservarTickets(GenericViewSet, CreateModelMixin):
    queryset = Tickets.objects.all()
    serializer_class = ReservarTicketSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        rota = Rota.objects.get(pk=serializer.data["rota"])
        user_soticon = UserSoticon.objects.get(usuario=request.user)

        ticket_reservado = Tickets.objects.filter(
            reservado=True, rota=rota, user_soticon=user_soticon
        )

        if ticket_reservado:
            Tickets.objects.update(reservado=False)

            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            ticket_desreservado = (
                Tickets.objects.filter(reservado=False, rota=rota)
                .order_by("posicao_fila")
                .first()
            )

            serializer_data = serializer.data

            if ticket_desreservado:

                ticket_desreservado.reservado = True
                ticket_desreservado.user_soticon = user_soticon
                ticket_desreservado.save()

                serializer_data["posicao_fila"] = (
                    ticket_desreservado.posicao_fila.num_ticket
                )

            else:

                try:
                    posicaofilaMax = (
                        Tickets.objects.filter(rota=rota)
                        .order_by("-posicao_fila")
                        .first()
                        .posicao_fila.num_ticket
                    ) + 1

                except:
                    posicaofilaMax = 1

                Tickets.objects.create(
                    usado=False,
                    reservado=True,
                    posicao_fila=PosicaoFila.objects.get(pk=posicaofilaMax),
                    rota=rota,
                    user_soticon=user_soticon,
                )

                serializer_data["posicao_fila"] = posicaofilaMax

            headers = self.get_success_headers(serializer_data)
            return Response(
                serializer_data, status=status.HTTP_201_CREATED, headers=headers
            )
