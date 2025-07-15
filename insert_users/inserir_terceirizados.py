import openpyxl
from django.db import transaction
from django.contrib.auth.hashers import make_password
from datetime import datetime as dt
import re
import datetime
import os
import sys
import django
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cortex.settings')
django.setup()


def ler_xlsx_para_dicionario(caminho_arquivo):
    workbook = openpyxl.load_workbook(caminho_arquivo)
    sheet = workbook.active

    cabecalhos = [cell.value for cell in sheet[1]]

    dados = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if all(cell is None for cell in row):
            continue

        linha_dict = {cabecalhos[i]: row[i] for i in range(len(cabecalhos))}
        dados.append(linha_dict)

    return dados


def main():
    caminho_arquivo = "insert_users/terceirizados.xlsx"
    dados_xlsx = ler_xlsx_para_dicionario(caminho_arquivo)
    dados = []
    for linha in dados_xlsx:
        data_nascimento = linha["Data de nascimento"]

        dict_to_append = {
            "cpf": re.sub("[^0-9]", "", str(linha["CPF"])),
            "nome": linha["Nome"],
            "setor": linha["Setor"],
            "cnpj_empresa": re.sub("[^0-9]", "", linha["CNPJ"]),
            "data_nascimento": data_nascimento if data_nascimento else None,
            "nome_empresa": linha["Razão Social"],
            "email": linha["Email"],
        }

        dados.append(dict_to_append)

    with transaction.atomic():
        from gerUsuarios.models import User, Contato, Tipo, Endereco, Setor, Empresa

        for dado in dados:
            tipo = Tipo.objects.get(nome="Serv.Terceirizado".lower())
            setor = Setor.objects.get(nome=dado["setor"].lower())

            empresa, created = Empresa.objects.get_or_create(
                cnpj=dado["cnpj_empresa"],
                defaults={
                    "nome": dado["nome_empresa"],
                }
            )

            user, created = User.objects.get_or_create(
                cpf=dado["cpf"],
                defaults={
                    "nome": dado["nome"],
                    "email": f"{dado['cpf']}@servidores.fakeemail.com",
                    "password": make_password(dado["cpf"]),
                    "tipo": tipo,
                    "empresa": empresa,
                    "data_nascimento": dado["data_nascimento"],
                }
            )

            user.setores.set([setor])
            user.save()


if __name__ == "__main__":
    main()
