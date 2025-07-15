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
    caminho_arquivo = "insert_users/servidores.xlsx"
    dados_xlsx = ler_xlsx_para_dicionario(caminho_arquivo)
    dados = []
    for linha in dados_xlsx:
        email = linha["Email Institucional"] if linha[
            "Email Institucional"] else f"{linha['Matrícula']}@servidores.ifpi.edu.br"

        dict_to_append = {
            "login_cpf": re.sub("[^0-9]", "", linha["Matrícula"]),
            "nome": linha["Nome"],
            "matricula": linha["Matrícula"],
            "email_institucional": email,
            "setor": linha["Cargo"],
            "tipo": linha["Setor Exercício"],
        }

        dados.append(dict_to_append)

    with transaction.atomic():
        from gerUsuarios.models import User, Setor_User, Tipo, Matricula, Setor

        for dado in dados:
            tipo = Tipo.objects.get(nome=dado["tipo"].lower())
            setor = Setor.objects.get(nome=dado["setor"].lower())

            user, created = User.objects.get_or_create(
                cpf=dado["login_cpf"],
                defaults={
                    "nome": dado["nome"],
                    "email": dado["email_institucional"],
                    "password": make_password(dado["matricula"]),
                    "tipo": tipo,
                }
            )

            matricula, created = Matricula.objects.get_or_create(
                matricula=dado["matricula"],
                expedicao=datetime.datetime.now(),
                user=user,
            )

            user.setores.set([setor])
            user.save()


if __name__ == "__main__":
    main()
