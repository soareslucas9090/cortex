from datetime import date, datetime, timedelta

from django.db.models import Case, IntegerField, Value, When
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from gerUsuarios.permissions import IsAdminOrTI

from .models import *
from .permissions import (
    IsAuthorizedToOperateRoutes,
    IsSectorAuthorizedToChangeRoutes,
    IsStudent,
)
from .serializers import *


@extend_schema(tags=["Soticon.UsersSoticon"])
class UserSoticonViewSet(ModelViewSet):
    queryset = UserSoticon.objects.all()
    serializer_class = UserSoticonSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head"]

    def retrieve(self, request, *args, **kwargs):
        user_soticon = UserSoticon.objects.get(usuario=request.user.id)

        if int(kwargs.get("pk")) != user_soticon.id:
            if not IsAdminOrTI().has_permission(self.request, self):
                return Response(
                    {"Usuário sem permição de visualização destes dados."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        instance = self.get_object()
        return self.listarTicketsDoUsuario(instance)

    def list(self, request, *args, **kwargs):
        try:
            queryset = super().get_queryset()
            if not IsAdminOrTI().has_permission(self.request, self):
                queryset = queryset.get(usuario=self.request.user)
                return self.listarTicketsDoUsuario(queryset)

            return super().list(request, *args, **kwargs)

        except Exception as e:
            print(e)

    def listarTicketsDoUsuario(self, instance):
        serializer = self.get_serializer(instance)
        serializer.data["tickets_reservados"] = []

        data_atual = date.today()
        ticket_reservado = Tickets.objects.filter(
            user_soticon=instance, reservado=True, usado=False, rota__data=data_atual
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

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE", "POST"]:
            return [IsAdminOrTI()]

        return super().get_permissions()


@extend_schema(tags=["Soticon.Strikes"])
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="nome",
                type=OpenApiTypes.STR,
                description="Filtra os strikes de um usuario pelo nome dele",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE", "POST"]:
            return [IsAdminOrTI()]

        return super().get_permissions()


@extend_schema(tags=["Soticon.Justificativas"])
class JustificativaViewSet(ModelViewSet):
    queryset = Justificativa.objects.all()
    serializer_class = JustificativaSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


@extend_schema(tags=["Soticon.PosicaoFila"])
class PosicaoFilaViewSet(ModelViewSet):
    queryset = PosicaoFila.objects.all()
    serializer_class = PosicaoFilaSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


@extend_schema(tags=["Soticon.Rotas"])
class RotaViewSet(ModelViewSet):
    queryset = Rota.objects.all()
    serializer_class = RotaSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head", "put", "delete", "post"]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="status",
                type=OpenApiTypes.STR,
                description="Filtra as rotas pelo status",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="gte",
                type=OpenApiTypes.BOOL,
                description="Filtra as rotas a partir do dia de pesquisa",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="data",
                type=OpenApiTypes.STR,
                description="Filtra as rotas pela data",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="data_inicial",
                type=OpenApiTypes.STR,
                description="Filtra as rotas entre a data inicial e a data final (deve ser usada junto a data_final)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="data_final",
                type=OpenApiTypes.STR,
                description="Filtra as rotas entre a data inicial e a data final (deve ser usada junto a data_inicial)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="data_valida",
                type=OpenApiTypes.STR,
                description="Filtra as rotas pela data e por ainda estar válida para reserva",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        ######## Filtro de data geral ########
        status = self.request.query_params.get("status", None)

        if status:
            queryset = queryset.filter(status=status)

        ######## Filtro de data geral ########

        data = self.request.query_params.get("data")
        format = "%Y-%m-%d"
        data_formatada = None

        try:
            data_formatada = datetime.strptime(data, format)
        except:
            data_formatada = None

        if data_formatada:
            queryset = queryset.filter(data=data_formatada)

        ######## Filtro de intervalo de data ########

        data_inicial = self.request.query_params.get("data_inicial")
        data_final = self.request.query_params.get("data_final")
        format = "%Y-%m-%d"
        data_inicial_formatada = None
        data_final_formatada = None

        try:
            data_inicial_formatada = datetime.strptime(data_inicial, format)
            data_final_formatada = datetime.strptime(data_final, format)
        except:
            data_inicial_formatada = None
            data_final_formatada = None

        if data_inicial_formatada and data_final_formatada:
            queryset = queryset.filter(
                data__range=(data_inicial_formatada, data_final_formatada)
            )

        ######## Filtro de rotas a partir de hoje ########

        a_partir_de_hoje = self.request.query_params.get("gte", None)

        if a_partir_de_hoje:
            if a_partir_de_hoje.lower() == "false":
                a_partir_de_hoje = False

            elif a_partir_de_hoje.lower() == "true":
                a_partir_de_hoje = True

        if a_partir_de_hoje:
            queryset = queryset.filter(data__gte=datetime.now())

        ######## Filtro de data para rotas válidas para agendamento ########

        data_valida = self.request.query_params.get("data_valida")
        data_valida_formatada = None

        try:
            data_valida_formatada = datetime.strptime(data_valida, format)
        except:
            data_valida_formatada = None

        minutos_permitidos = Regras.objects.get(
            descricao="tempo_ate_fechamento_reservas"
        )

        if data_valida_formatada:
            if not self.request.user.deficiencia:
                horario_permitido = datetime.now() + timedelta(
                    minutes=minutos_permitidos.parametro
                )

            else:
                horario_permitido = datetime.now()

            queryset = queryset.filter(
                data=data_valida_formatada,
                status="espera",
                horario__gte=horario_permitido,
            )

        return queryset

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE", "POST"]:
            return [IsSectorAuthorizedToChangeRoutes()]

        return super().get_permissions()


@extend_schema(tags=["Soticon.Regras"])
class RegrasViewSet(ModelViewSet):
    queryset = Regras.objects.all()
    serializer_class = RegrasSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get"]


@extend_schema(
    tags=["Soticon.Tickets"],
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            examples=[
                OpenApiExample(
                    'Exemplo de Resposta Detalhada com query parameter "rota_valida" ou "usuario"',
                    value={
                        "id": 1,
                        "nome": "João da Silva",
                        "cpf": "12345678900",
                        "rota": 123,
                        "user_soticon": 456,
                        "posicao_fila": 5,
                        "usado": False,
                        "reservado": True,
                        "faltante": False,
                    },
                ),
                OpenApiExample(
                    "Exemplo de Resposta padrão",
                    value={
                        "id": 1,
                        "rota": 123,
                        "user_soticon": 456,
                        "posicao_fila": 5,
                        "usado": False,
                        "reservado": True,
                        "faltante": False,
                    },
                ),
            ]
        ),
    },
)
class TicketsViewSet(ModelViewSet):
    queryset = Tickets.objects.select_related("user_soticon__usuario").all()
    serializer_class = TicketsSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "head"]

    def get_queryset(self):
        queryset = super().get_queryset()

        usuario = self.request.query_params.get("usuario", None)

        if IsStudent().has_permission(self.request, self):
            if usuario:
                try:
                    user_soticon = UserSoticon.objects.get(id=usuario)
                    if user_soticon.usuario == self.request.user:
                        data_atual = date.today()
                        queryset = queryset.filter(
                            user_soticon=usuario,
                            usado=False,
                            reservado=True,
                            rota__data=data_atual,
                            rota__status="espera",
                        )

                        return queryset
                except:
                    pass

            return queryset.filter(id=0)

        if usuario:
            data_atual = date.today()
            queryset = queryset.filter(
                user_soticon=usuario,
                usado=False,
                reservado=True,
                rota__data=data_atual,
                rota__status="espera",
            )

        rota = self.request.query_params.get("rota", None)

        if rota and rota.isnumeric():
            queryset = queryset.filter(rota=rota)
            return queryset

        rota_valida = self.request.query_params.get("rota_valida", None)

        faltantes = self.request.query_params.get("faltantes", None)

        if faltantes:
            if faltantes.lower() == "false":
                faltantes = False

            elif faltantes.lower() == "true":
                faltantes = True

        if rota_valida and rota_valida.isnumeric() and faltantes:
            queryset = (
                queryset.filter(rota=rota_valida, reservado=True, faltante=True)
                .annotate(
                    deficiencia_priority=Case(
                        When(
                            user_soticon__usuario__deficiencia__isnull=False,
                            then=Value(0),
                        ),
                        default=Value(1),
                        output_field=IntegerField(),
                    )
                )
                .order_by(
                    "usado",
                    "deficiencia_priority",
                    "posicao_fila",
                )
            )
            return queryset

        elif rota_valida and rota_valida.isnumeric():

            todos = self.request.query_params.get("todos", None)

            if todos:
                if todos.lower() == "true":
                    queryset = queryset.filter(
                        rota=rota_valida, reservado=True
                    ).order_by("posicao_fila")
                return queryset

            queryset = (
                queryset.filter(rota=rota_valida, reservado=True, faltante=False)
                .annotate(
                    deficiencia_priority=Case(
                        When(
                            user_soticon__usuario__deficiencia__isnull=False,
                            then=Value(0),
                        ),
                        default=Value(1),
                        output_field=IntegerField(),
                    )
                )
                .order_by(
                    "usado",
                    "deficiencia_priority",
                    "posicao_fila",
                )
            )

            return queryset

        return queryset

    @extend_schema(
        description="Os tickets pesquisados por rota_valida ou usuario vêm com mais detalhes",
        parameters=[
            OpenApiParameter(
                name="rota",
                type=OpenApiTypes.INT,
                description="Filtras os tickets de determinada rota",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="contagem",
                type=OpenApiTypes.BOOL,
                description="Quando True, retorna o número totais de tickets reservados e tickets usados, precisa ser usado junto com ?rota=X",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="rota_valida",
                type=OpenApiTypes.INT,
                description="Filtra os tickets efetivamente reservados para uma determinada rota",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="faltantes",
                type=OpenApiTypes.BOOL,
                description="Filtra os tickets de usuários faltantes para uma rota válida (use junto com rota_valida)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="todos",
                type=OpenApiTypes.BOOL,
                description="Filtra todos os tickets de usuários para uma rota válida (use junto com rota_valida)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="usuario",
                type=OpenApiTypes.INT,
                description="Filtra todos os tickets de determinado usuário que não foram usados para a data de hoje",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        contagem = self.request.query_params.get("contagem", None)

        if contagem:

            rota = self.request.query_params.get("rota", None)

            if contagem.lower() == "true" and rota and rota.isnumeric():
                usados = self.queryset.filter(usado=True, rota=rota).count()
                total = self.queryset.filter(reservado=True, rota=rota).count()

                dict = {
                    "usados": usados,
                    "total": total,
                }

                return Response(dict, status=status.HTTP_200_OK)

        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.query_params.get("rota_valida", None):
            return TicketsDetalhadosParaVerificacaoSerializer

        elif self.request.query_params.get("usuario", None):
            try:
                return TicketsDetalhadosParaDetalhesUsuarioSerializer
            except Exception as e:
                print(e)

        return self.serializer_class


@extend_schema(tags=["Soticon.Reservar Tickets"])
class ReservarTickets(GenericViewSet, CreateModelMixin):
    queryset = Tickets.objects.all()
    serializer_class = ReservarTicketSerializer
    permission_classes = [
        IsStudent,
    ]
    http_method_names = ["post"]

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(description="Ticket reservado"),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Rota não válida"),
            status.HTTP_406_NOT_ACCEPTABLE: OpenApiResponse(
                description="Rota não disponível"
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="Internal Error"
            ),
        }
    )
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

                        while True:
                            try:
                                Tickets.objects.create(
                                    usado=False,
                                    reservado=True,
                                    posicao_fila=PosicaoFila.objects.get(
                                        pk=posicaofilaMax
                                    ),
                                    rota=rota,
                                    user_soticon=user_soticon,
                                )
                                break
                            except:
                                posicaofilaMax += 1

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


@extend_schema(
    tags=["Soticon.Verificar Tickets"],
    responses={
        status.HTTP_200_OK: OpenApiResponse(description="Ticket Verificado"),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="A posição do ticket que está sendo verificado não corresponde a esperada/O usuário já usou o ticket"
        ),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Ticket não localizado"),
        status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
            description="Erro interno."
        ),
    },
)
class VerificarTickets(ModelViewSet):
    queryset = Tickets.objects.all()
    http_method_names = ["put"]
    permission_classes = [IsAuthorizedToOperateRoutes]

    def ticket_verificado(self, ticket):
        ticket.usado = True
        ticket.faltante = False
        ticket.save()

        return Response(
            {"message": "Ticket verificado com sucesso!"},
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        try:
            ticket = Tickets.objects.get(pk=kwargs["pk"])

            if not ticket.reservado:
                return Response(
                    {"error": "Usuário não possui reserva!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if ticket.usado:
                return Response(
                    {"error": "Usuário já usou o ticket."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:

                posicao_esperada = (
                    Tickets.objects.filter(
                        rota=ticket.rota, reservado=True, faltante=False, usado=False
                    )
                    .annotate(
                        deficiencia_priority=Case(
                            When(
                                user_soticon__usuario__deficiencia__isnull=False,
                                then=Value(0),
                            ),
                            default=Value(1),
                            output_field=IntegerField(),
                        )
                    )
                    .order_by(
                        "deficiencia_priority",
                        "posicao_fila",
                    )
                    .first()
                )

                if posicao_esperada.posicao_fila == ticket.posicao_fila:
                    return self.ticket_verificado(ticket)

                print("aqui")
                return Response(
                    {
                        "error": "A posição do ticket que está sendo verificado não corresponde a esperada.",
                        "posicao_esperada": posicao_esperada.posicao_fila.num_ticket,
                        "posicao_passada": ticket.posicao_fila.num_ticket,
                    },
                    status=400,
                )

            except Exception as e:
                print(e)

        except Tickets.DoesNotExist:
            return Response(
                {"error": "Ticket não encontrado"}, status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(
    tags=["Soticon.Verificar Tickets"],
    examples=[
        OpenApiExample(
            "Exemplo requisição correta.",
            value={
                "user_soticon": 9,
                "rota": 220,
            },
        )
    ],
    responses={
        status.HTTP_200_OK: OpenApiResponse(description="Ticket Verificado"),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="O usuário não é faltante/O usuário já usou o ticket/O usuário não possui reserva"
        ),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            description="Usuário não localizado/Usuário não possui reserva/Rota não localizada."
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
            description="Erro interno."
        ),
    },
)
class VerificarTicketsFaltantes(ModelViewSet):
    queryset = Tickets.objects.all()
    http_method_names = ["put"]
    permission_classes = [IsAuthorizedToOperateRoutes]

    def update(self, request, *args, **kwargs):
        try:
            ticket = Tickets.objects.get(pk=kwargs["pk"])

            if not ticket.reservado:
                return Response(
                    {"error": "Usuário não possui reserva!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if ticket.usado:
                return Response(
                    {"error": "Usuário já usou o ticket."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not ticket.faltante:
                return Response(
                    {"error": "Usuário não é faltante."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            ticket.usado = True
            ticket.faltante = False
            ticket.save()

            return Response(
                {"message": "Ticket verificado com sucesso!"},
                status=status.HTTP_200_OK,
            )

        except Tickets.DoesNotExist:
            return Response(
                {"error": "Ticket não encontrado"}, status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(
    tags=["Soticon.Declarar Aluno Faltante"],
    responses={
        status.HTTP_200_OK: OpenApiResponse(description="Ticket Atualizado"),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="O usuário já usou o ticket/O usuário não possui reserva"
        ),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Ticket não localizado"),
        status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
            description="Erro interno."
        ),
    },
)
class DeclararAlunoFaltante(ModelViewSet):
    queryset = Tickets.objects.all()
    http_method_names = ["put"]
    permission_classes = [IsAuthorizedToOperateRoutes]

    def update(self, request, *args, **kwargs):
        try:
            ticket = Tickets.objects.get(pk=kwargs["pk"])

            if not ticket.reservado:
                return Response(
                    {"error": "Usuário não possui reserva!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if ticket.usado:
                return Response(
                    {"error": "Usuário já usou o ticket."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            ticket.faltante = True
            ticket.usado = False
            ticket.save()

            return Response(
                {"message": "Ticket atualizado com sucesso!"},
                status=status.HTTP_200_OK,
            )

        except Tickets.DoesNotExist:
            return Response(
                {"error": "Ticket não encontrado"}, status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(tags=["Soticon.Finalizar Rota"])
class FinalizarRota(ModelViewSet):
    queryset = Rota.objects.all()
    serializer_class = FinalizarRotaSerializer
    permission_classes = [
        IsAuthorizedToOperateRoutes,
    ]
    http_method_names = ["put"]

    def get_object(self, request, **kwargs):
        if "pk" in kwargs:
            try:
                rota_id = kwargs["pk"]
                try:
                    rota_soticon = Rota.objects.get(pk=rota_id)
                    return rota_soticon

                except Rota.DoesNotExist:
                    return None

            except Exception as e:
                print(e)
                return Response(
                    {"result": "Erro ao realizar consulta de dados"}, status=500
                )

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object(request, **kwargs)
        if instance is None:
            return Response({"result": "Rota não localizada"}, status=404)

        dados = request.data

        if dados["status"].lower() == "executada":
            embarques_sem_tickets = dados.get("embarques_sem_tickets", None)

            if not embarques_sem_tickets and embarques_sem_tickets != 0:
                return Response(
                    {"result": 'Informe um valor inteiro para "embarques_sem_tickets"'},
                    status=400,
                )

            instance.status = "executada"
            instance.embarques_sem_tickets = embarques_sem_tickets
            instance.save()

        else:
            if dados["obs"]:
                obs = dados["obs"]
            else:
                obs = ""

            instance.status = "cancelada"
            instance.obs = obs
            instance.save()

        return Response({"result": "Rota finalizada"}, status=status.HTTP_200_OK)


@extend_schema(tags=["Soticon.Rotas Automáticas"])
class RotasAutomaticasViewSet(ModelViewSet):
    queryset = RotasAutomaticas.objects.all()
    serializer_class = RotasAutomaticasSerializer
    permission_classes = [
        IsSectorAuthorizedToChangeRoutes,
    ]
    http_method_names = ["get", "post", "put", "delete"]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="dia",
                type=OpenApiTypes.STR,
                description="Filtra as rotas automáticas pelo dia da semana.",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        dia_da_semana = self.request.query_params.get("dia", None)

        if dia_da_semana:
            queryset = queryset.filter(dia_da_semana=dia_da_semana)

        return queryset


@extend_schema(tags=["Soticon.Rotas Automáticas"])
class CriarRotasAutomaticas(ModelViewSet):
    queryset = RotasAutomaticas.objects.all()
    permission_classes = [
        IsSectorAuthorizedToChangeRoutes,
    ]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        try:
            DIA_SEMANA_MAP = {
                "segunda": 0,
                "terça": 1,
                "quarta": 2,
                "quinta": 3,
                "sexta": 4,
                "sabado": 5,
                "domingo": 6,
            }
            hoje = date.today()
            rotas_automaticas = RotasAutomaticas.objects.all()
            rotas_criadas = []

            for rota_automatica in rotas_automaticas:
                dia_semana_numero = DIA_SEMANA_MAP.get(
                    rota_automatica.dia_da_semana.lower()
                )

                dias_para_proximo_dia = (dia_semana_numero - hoje.weekday()) % 7

                proxima_data = hoje + timedelta(days=dias_para_proximo_dia)

                try:
                    rota_existente = Rota.objects.get(
                        data=proxima_data,
                        horario=rota_automatica.horario,
                        status="espera",
                    )

                    if rota_existente:
                        continue

                except Rota.DoesNotExist:
                    nova_rota = Rota.objects.create(
                        obs="Rota Automática",
                        data=proxima_data,
                        horario=rota_automatica.horario,
                        status="espera",
                    )
                    rotas_criadas.append(nova_rota)

            return Response(
                {
                    "success": "Rotas criadas com sucesso!",
                    "rotas_criadas": [
                        {"id": rota.id, "data": rota.data, "horario": rota.horario}
                        for rota in rotas_criadas
                    ],
                }
            )

        except Exception as e:
            print(e)


@extend_schema(tags=["Soticon.Rotas"])
class RelatorioRotasViewSet(GenericViewSet, RetrieveModelMixin):
    queryset = Rota.objects.all()
    serializer_class = RelatorioRotasSerializer
    permission_classes = [
        IsSectorAuthorizedToChangeRoutes,
    ]
    http_method_names = ["get"]

    def retrieve(self, request, *args, **kwargs):
        try:
            rota = get_object_or_404(Rota, pk=kwargs["pk"])

            if rota.status != "executada":
                return Response(
                    {"error": 'O status da rota precisa ser "executada".'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = {}
            data["data"] = rota.data
            data["horario"] = rota.horario
            data["emitidos"] = Tickets.objects.filter(rota=rota, reservado=True).count()
            data["confirmados"] = Tickets.objects.filter(rota=rota, usado=True).count()
            data["faltantes"] = Tickets.objects.filter(
                rota=rota, reservado=True, faltante=True
            ).count()

            if rota.embarques_sem_tickets:
                data["sem_ticket"] = rota.embarques_sem_tickets
            else:
                data["sem_ticket"] = 0

            data["total"] = data["confirmados"] + data["sem_ticket"]

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
