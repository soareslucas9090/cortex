from django.apps import AppConfig
from django.db import OperationalError
from django.db.models.signals import post_migrate


class GerusuariosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gerUsuarios"

    def ready(self):
        from .models import Empresa, Setor, Tipo

        post_migrate.connect(create_default_tipos, sender=self)
        post_migrate.connect(create_default_setores, sender=self)
        post_migrate.connect(create_default_empresa, sender=self)


def create_default_tipos(sender, **kwargs):
    Tipo = sender.get_model("Tipo")
    default_tipos = [
        "Admin",
        "TI",
        "Aluno",
        "Motorista",
        "Professor",
        "Diretor.Geral",
        "Diretor.Ensino",
        "Coordenador",
        "Tec.Administrativo",
        "Serv.Terceirizado",
    ]

    for name_tipo in default_tipos:
        try:
            Tipo.objects.get_or_create(nome=name_tipo.lower())
        except OperationalError:
            print("Não foi possível realizar migrate de dados de Tipos")
            pass


def create_default_setores(sender, **kwargs):
    Setor = sender.get_model("Setor")
    default_setor = [
        "Alunos",
        "Direcao Geral",
        "Direcao de Ensino",
        "Direcao de Administracao e Planejamento",
        "Coordenacao Informatica",
        "Coordenacao Tec Informatica",
        "Coordenacao Eletromecanica",
        "Coordenacao Tec Eletromecanica",
        "Coordenacao Edificacoes",
        "Coordenacao Tec Edificacoes",
        "Coordenacao Meio Ambiente",
        "Coordenacao Tec Meio Ambiente",
        "Coordenacao TADS",
        "Coordenacao Biologia",
        "Coordenacao Matematica",
        "Coordenacao PROFMAT",
        "Coordenacao de Compras e Licitacao",
        "Coordenacao de Controle Academico",
        "Coordenacao de Disciplina",
        "Coordenacao de Ed. Fisica",
        "Coordenacao de Extensao",
        "Coordenacao de Multimidia",
        "Coordenacao de Patrimônio e Almoxarifado",
        "Coordenacao de Pesquisa e Inovacao",
        "TI",
        "Biblioteca",
        "Casa da Leitura",
        "Departamento Contabilidade",
        "Departamento Apoio ao Ensino",
        "Departamento Logistica, Manutencao e Compras",
        "Enfermagem",
        "Engenharia",
        "Nutricao",
        "Psicologia",
        "Saude",
        "Servico Social",
        "Medico",
        "Odontologico",
        "Pedagogico",
        "Refeitorio",
        "Guarita",
        "Area Externa",
    ]

    for name_setor in default_setor:
        try:
            Setor.objects.get_or_create(nome=name_setor.lower())
        except OperationalError:
            print("Não foi possível realizar migrate de dados de Setores")
            pass


def create_default_empresa(sender, **kwargs):
    Empresa = sender.get_model("Empresa")

    try:
        Empresa.objects.get(cnpj="10806496000491")
    except:
        Empresa.objects.create(cnpj="10806496000491", nome="IFPI - Campus Floriano")
        pass
