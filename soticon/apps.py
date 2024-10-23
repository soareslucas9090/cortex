from django.apps import AppConfig, apps
from django.db import OperationalError
from django.db.models.signals import post_migrate


class SoticonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "soticon"

    def ready(self):
        from gerUsuarios.models import User

        from .models import PosicaoFila, Regras, UserSoticon

        post_migrate.connect(create_default_posicoes_fila, sender=self)
        post_migrate.connect(create_default_users_soticon, sender=self)
        post_migrate.connect(create_default_regras_soticon, sender=self)


def create_default_posicoes_fila(sender, **kwargs):
    Posicao = sender.get_model("PosicaoFila")

    for i in range(150):
        try:
            Posicao.objects.get_or_create(num_ticket=(i + 1))
        except OperationalError:
            print("Não foi possível realizar migrate das Posições")
            pass


def create_default_users_soticon(sender, **kwargs):
    Users = apps.get_model("gerUsuarios", "User")
    Users_Soticon = sender.get_model("UserSoticon")

    users_sem_soticon = Users.objects.filter(
        user_soticon__isnull=True, tipo__nome="aluno"
    )

    for user in users_sem_soticon:
        try:
            Users_Soticon.objects.create(usuario=user, faltas=0)
        except OperationalError:
            print("Não foi possível realizar migrate dos usuários Soticon")
            pass


def create_default_regras_soticon(sender, **kwargs):
    Regras = sender.get_model("Regras")

    try:
        # Regra de quantidade de vagas no onibus
        try:
            Regras.objects.get(descricao="num_vagas_onibus")
        except:
            Regras.objects.create(descricao="num_vagas_onibus", parametro=84)

        # Regra de tempo para o fechamento das reservas de tickets
        try:
            Regras.objects.get(descricao="tempo_ate_fechamento_reservas")
        except:
            Regras.objects.create(
                descricao="tempo_ate_fechamento_reservas", parametro=30
            )

    except OperationalError:
        print("Não foi possível realizar migrate das regras do Soticon")
        pass
