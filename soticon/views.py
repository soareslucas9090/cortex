from datetime import date, datetime, timedelta

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
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

        ######## Filtro de rotas a partir de hoje ########

        a_partir_de_hoje = self.request.query_params.get("gte", None)

        if a_partir_de_hoje:
            if a_partir_de_hoje.lower() == "false":
                a_partir_de_hoje = False

            elif a_partir_de_hoje.lower() == "true":
                a_partir_de_hoje = True

        if a_partir_de_hoje:
            return queryset.filter(data__gte=datetime.now())

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

    @extend_schema(
        description="Retorna dados dos tickets reservados para aquela rota também.",
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        serializer.data["tickets"] = []

        tickets = Tickets.objects.filter(rota=instance, reservado=True)

        if tickets:
            tickets_reservados = []

            for ticket in tickets:

                ticket_data = {
                    "user": [
                        {
                            "id": ticket.user_soticon.id,
                            "nome": ticket.user_soticon.usuario.nome,
                        }
                    ],
                    "usado": ticket.usado,
                    "num_ticket": ticket.posicao_fila.num_ticket,
                }

                tickets_reservados.append(ticket_data)

            serializer.data["tickets"] = tickets_reservados

        return Response(serializer.data)

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

        if IsStudent().has_permission(self.request, self):
            return queryset.filter(id=0)

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
            queryset = queryset.filter(
                rota=rota_valida, reservado=True, faltante=True
            ).order_by("usado", "posicao_fila")
            return queryset

        elif rota_valida and rota_valida.isnumeric():
            queryset = queryset.filter(
                rota=rota_valida, reservado=True, faltante=False
            ).order_by("usado", "posicao_fila")
            return queryset

        usuario = self.request.query_params.get("usuario", None)

        if usuario:
            data_atual = date.today()
            queryset = queryset.filter(
                user_soticon=usuario, usado=False, reservado=True, rota__data=data_atual
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
                name="usuario",
                type=OpenApiTypes.INT,
                description="Filtra todos os tickets de determinado usuário que não foram usados para a data de hoje",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.query_params.get(
            "rota_valida", None
        ) or self.request.query_params.get("usuario", None):
            return TicketsDetalhadosSerializer

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

                if ticket.posicao_fila.num_ticket == 1:
                    return self.ticket_verificado(ticket)

                algum_aluno_passou = Tickets.objects.filter(
                    rota=ticket.rota, usado=True
                )

                if not algum_aluno_passou:
                    aluno_faltante = (
                        Tickets.objects.filter(rota=ticket.rota, faltante=True)
                        .order_by("-posicao_fila")
                        .first()
                    )

                    if (
                        aluno_faltante
                        and ticket.posicao_fila.num_ticket
                        == aluno_faltante.posicao_fila.num_ticket + 1
                    ):
                        return self.ticket_verificado(ticket)

                    posicao_esperada = 1

                    if aluno_faltante:
                        posicao_esperada = aluno_faltante.posicao_fila.num_ticket + 1

                    return Response(
                        {
                            "error": "A posição do ticket que está sendo verificado não corresponde a esperada.",
                            "posicao_esperada": posicao_esperada,
                            "posicao_passada": ticket.posicao_fila.num_ticket,
                        },
                        status=400,
                    )

                fila = Tickets.objects.filter(rota=ticket.rota)

                fila = (
                    fila.exclude(usado=False, faltante=False)
                    .order_by("-posicao_fila")
                    .first()
                )

                if fila and ticket.posicao_fila.num_ticket == (
                    fila.posicao_fila.num_ticket + 1
                ):
                    return self.ticket_verificado(ticket)

                posicao_esperada = 0

                if fila:
                    posicao_esperada = fila.posicao_fila.num_ticket + 1

                return Response(
                    {
                        "error": "A posição do ticket que está sendo verificado não corresponde a esperada.",
                        "posicao_esperada": posicao_esperada,
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
            instance.status = "executada"
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
