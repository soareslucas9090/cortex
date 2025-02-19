from django.db import models

from gerUsuarios import models as modelsUsusarios

# Pensar em Signals como gatilhos se precisar


class UserSoticon(modelsUsusarios.Base):
    usuario = models.OneToOneField(
        modelsUsusarios.User,
        related_name="user_soticon",
        on_delete=models.CASCADE,
        null=False,
    )
    faltas = models.IntegerField(null=False)

    def __str__(self):
        str = f"{self.usuario.nome}"
        return str


class Strike(modelsUsusarios.Base):
    user_soticon = models.ForeignKey(
        UserSoticon,
        related_name="strike_user_soticon",
        on_delete=models.CASCADE,
        null=False,
    )
    data = models.DateField(auto_now_add=True, null=False)

    def __str__(self):
        str = f"{self.user_soticon.nome}"
        return str


class Justificativa(modelsUsusarios.Base):
    strike = models.ForeignKey(
        Strike,
        related_name="justificativa_strike",
        on_delete=models.CASCADE,
        null=False,
    )
    data = models.DateField(auto_now_add=True, null=False)
    obs = models.CharField(max_length=512, null=False)

    def __str__(self):
        str = f"{self.strike}"
        return str


class PosicaoFila(modelsUsusarios.Base):
    num_ticket = models.IntegerField(null=False, unique=True)

    def __str__(self):
        str = f"{self.num_ticket}"
        return str


class Rota(modelsUsusarios.Base):
    obs = models.CharField(max_length=512)
    data = models.DateField(null=False)
    status = models.CharField(max_length=30, null=False)
    horario = models.TimeField(null=False)
    embarques_sem_tickets = models.IntegerField(null=True)

    def __str__(self):
        str = f"{self.horario}"
        return str

    class Meta:
        ordering = ["-data"]


class RotasAutomaticas(models.Model):
    DIAS_DA_SEMANA = [
        ("segunda", "Segunda-feira"),
        ("terca", "Terça-feira"),
        ("quarta", "Quarta-feira"),
        ("quinta", "Quinta-feira"),
        ("sexta", "Sexta-feira"),
        ("sabado", "Sábado"),
        ("domingo", "Domingo"),
    ]

    horario = models.TimeField(null=False)
    dia_da_semana = models.CharField(max_length=10, choices=DIAS_DA_SEMANA, null=False)

    def __str__(self):
        return f"{self.dia_da_semana} às {self.horario}"


class Tickets(models.Model):
    rota = models.ForeignKey(
        Rota, related_name="tickets_rota", on_delete=models.RESTRICT, null=False
    )
    user_soticon = models.ForeignKey(
        UserSoticon,
        related_name="tickets_soticon",
        on_delete=models.CASCADE,
        null=False,
    )
    usado = models.BooleanField(default=False, null=False)
    reservado = models.BooleanField(default=False, null=False)
    posicao_fila = models.ForeignKey(
        PosicaoFila,
        related_name="tickets_posicao",
        on_delete=models.RESTRICT,
        null=False,
    )
    faltante = models.BooleanField(default=False, null=False)

    def __str__(self):
        str = f"Rota: {self.rota}, userSoticon: {self.user_soticon}"
        return str

    class Meta:
        ordering = ["rota"]

        constraints = [
            models.UniqueConstraint(
                fields=["rota", "posicao_fila"], name="unique_rota_posicao_constraint"
            )
        ]


class Regras(modelsUsusarios.Base):
    descricao = models.CharField(max_length=512, null=False, unique=True)
    parametro = models.IntegerField(null=False)
