from django.apps import AppConfig
from django.db import OperationalError
from django.db.models.signals import post_migrate


class GerusuariosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gerUsuarios"

    def ready(self):
        from .models import Empresa, Setor, Tipo

        post_migrate.connect(create_default_tipos, sender=self)


def create_default_tipos(sender, **kwargs):
    Tipo = sender.get_model("Tipo")
    default_tipos = [
        "Admin",
        "TI",
        "Aluno",
        "Professor",
        "Diretor Geral",
        "Diretor de Ensino",
        "Coordenador",
        "Motorista",
        "Tec. Administrativo",
        "Terceirizado",
    ]

    for name_tipo in default_tipos:
        try:
            Tipo.objects.get_or_create(name=name_tipo)
        except OperationalError:
            pass


def create_default_setores(sender, **kwargs):
    Setor = sender.get_model("Setor")
    default_setor = [
        "Direcao Geral",
        "Direcao de Ensino",
        "Docente",
        "Coordenacao Informatica",
        "Coordenacao Eletromecanica",
        "Coordenacao Edificacoes",
        "Coordenacao Meio Ambiente",
        "Coordenacao TADS",
        "Coordenacao Biologia",
        "Coordenacao Matematica",
        "Contabilidade",
        "Saude",
        "Multimeios",
        "CODIS",
        "Refeitorio",
        "Guarita",
    ]

    for name_setor in default_setor:
        try:
            Setor.objects.get_or_create(name=name_setor)
        except OperationalError:
            pass


def create_default_empresa(sender, **kwargs):
    Empresa = sender.get_model("Empresa")

    try:
        Empresa.objects.get_or_create(
            nome="IFPI - Campus Floriano", cnpj="10806496000491"
        )
    except OperationalError:
        pass
