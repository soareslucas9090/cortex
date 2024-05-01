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
from .serializers import *


class UserSoticonViewSet(ModelViewSet):
    queryset = UserSoticon.objects.all()
    serializer_class = UserSoticonSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return self.listarTicketsDoUsuario(instance)

    def list(self, request, *args, **kwargs):
        usuario = self.request.query_params.get("usuario", None)
        if usuario:
            queryset = super().get_queryset()
            queryset = queryset.get(usuario=usuario)
            print(queryset)
            return self.listarTicketsDoUsuario(queryset)

        else:
            return super().list(request, *args, **kwargs)

    def listarTicketsDoUsuario(self, instance):
        serializer = self.get_serializer(instance)
        serializer.data["tickets_reservados"] = []

        data_atual = date.today()
        ticket_reservado = Tickets.objects.filter(
            Q(user_soticon=instance, reservado=True, usado=False)
            & Q(rota__data=data_atual)
        )
        if ticket_reservado:
            serializer_data = serializer.data
            tickets_reservado = []

            for ticket in ticket_reservado:

                ticket_data = {
                    "rota": [
                        {
                            "id": ticket.rota.id,
                            "status": ticket.rota.status,
                            "data": ticket.rota.data,
                            "horario": ticket.rota.horario,
                        }
                    ],
                    "num_ticket": ticket.posicao_fila.num_ticket,
                }
                tickets_reservado.append(ticket_data)

            serializer_data["tickets_reservados"] = tickets_reservado

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

        ######## Filtro de data geral ########

        data = self.request.query_params.get("data")
        format = "%Y-%m-%d"
        data_formatada = None

        try:
            data_formatada = datetime.strptime(data, format)
        except:
            data_formatada = None

        if data_formatada:
            return queryset.filter(data=data_formatada)

        ######## Filtro de data para rotas válidas para agendamento ########

        data_valida = self.request.query_params.get("data_valida")
        data_valida_formatada = None

        try:
            data_valida_formatada = datetime.strptime(data_valida, format)
        except:
            data_valida_formatada = None

        horario_permitido = datetime.now() + timedelta(minutes=20)

        if data_valida_formatada:
            return queryset.filter(
                data=data_valida_formatada,
                status="espera",
                horario__gte=horario_permitido,
            )

        return queryset


class TicketsViewSet(ModelViewSet):
    queryset = Tickets.objects.select_related("user_soticon__usuario").all()
    serializer_class = TicketsSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.queryset.filter()

        rota = self.request.query_params.get("rota", None)

        if rota and rota.isnumeric():
            queryset = queryset.filter(rota=rota)
            return queryset

        rota_valida = self.request.query_params.get("rota_valida", None)

        if rota_valida and rota_valida.isnumeric():
            queryset = queryset.filter(rota=rota_valida, reservado=True)
            return queryset

        usuario = self.request.query_params.get("usuario", None)

        if usuario:
            data_atual = date.today()
            queryset = queryset.filter(
                user_soticon=usuario, usado=False, reservado=True, rota__data=data_atual
            )
            return queryset

        return queryset

    def get_serializer_class(self):
        if self.request.query_params.get(
            "rota_valida", None
        ) or self.request.query_params.get("usuario", None):
            return TicketsDetalhadosSerializer

        return self.serializer_class


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

        try:
            rota = Rota.objects.get(pk=serializer.data["rota"])

            if rota.status == "espera":

                user_soticon = UserSoticon.objects.get(usuario=request.user)

                ticket_reservado = Tickets.objects.filter(
                    reservado=True, rota=rota, user_soticon=user_soticon
                )

                if ticket_reservado:
                    ticket_reservado.update(reservado=False)
                    serializer_data = {"Resultado": "Ticket desreservado"}
                    serializer_data.update(serializer.data)
                    return Response(serializer_data, status=status.HTTP_200_OK)

                else:
                    ticket_desreservado = (
                        Tickets.objects.filter(reservado=False, rota=rota)
                        .order_by("posicao_fila")
                        .first()
                    )

                    serializer_data = {"Resultado": "Ticket reservado"}
                    serializer_data.update({"Usuario": request.user.nome})
                    serializer_data.update(serializer.data)

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

            else:
                erro = {"Erro": "A rota não está mais disponível!"}
                return Response(erro, status=status.HTTP_406_NOT_ACCEPTABLE)

        except Rota.DoesNotExist:
            erro = {"Erro": "A rota fornecida não é válida!"}
            return Response(erro, status=status.HTTP_404_NOT_FOUND)


class VerificarTickets(ModelViewSet):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer
    http_method_names = ["put"]
    permission_classes = [IsAuthenticated]

    def get_object(self, request):
        if "user_soticon" and "rota" in request.data:
            try:
                user_soticon = request.data.get("user_soticon")
                rota_id = request.data.get("rota")
                try:

                    UserSoticon.objects.get(pk=user_soticon)
                    Rota.objects.get(pk=rota_id)

                    reserva = Tickets.objects.filter(
                        user_soticon=user_soticon,
                        rota=rota_id,
                        usado=False,
                        reservado=True,
                    ).first()
                    return reserva

                except UserSoticon.DoesNotExist:
                    return Response("Usuário não localizado!", status=404)

                except Rota.DoesNotExist:
                    return Response("Rota não localizada!", status=404)

            except Exception as e:
                print(e)
                return Response("Erro ao realizar consulta de dados", status=500)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object(request)
        if instance is None:
            return Response("Usuário não possui reserva!", status=404)

        serializer = self.get_serializer(instance, data={"usado": True}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class FinalizarRota(ModelViewSet):
    queryset = Rota.objects.all()
    serializer_class = FinalizarRotaSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["put"]

    def get_object(self, request):
        if "rota" in request.data:
            try:
                rota_id = request.data.get("rota")

                try:

                    rota_soticon = Rota.objects.get(pk=rota_id)

                    rota = Rota.objects.filter(pk=rota_id)
                    return rota

                except Rota.DoesNotExist:
                    return Response("Rota não localizada!", status=404)

            except Exception as e:
                print(e)
                return Response("Erro ao realizar consulta de dados", status=500)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object(request)
        if instance is None:
            return Response("Rota não localizada", status=404)

        dados = request.data

        if dados["status"] == "sucesso":
            dict_dados = {"status": "executada"}
            instance.update(status=dict_dados["status"])

        else:
            if dados["obs"]:
                obs = dados["obs"]
            else:
                obs = ""

            dict_dados = {"status": "cancelada", "obs": obs}

            instance.update(status=dict_dados["status"], obs=dict_dados["obs"])

        return Response(
            {"Rota finalizada": request.data.get("rota")}, status=status.HTTP_200_OK
        )
