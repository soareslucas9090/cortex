from django.apps import AppConfig
from django.db import OperationalError
from django.db.models.signals import post_migrate


class SoticonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "soticon"

    def ready(self):
        from .models import PosicaoFila

        post_migrate.connect(create_default_posicoes_fila, sender=self)


def create_default_posicoes_fila(sender, **kwargs):
    Posicao = sender.get_model("PosicaoFila")

    for i in range(150):
        try:
            Posicao.objects.get_or_create(num_ticket=(i + 1))
        except OperationalError:
            print("Não foi possível realizar migrate das Posições")
            pass
