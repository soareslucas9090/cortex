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
    caminho_arquivo = "insert_users/alunos.xlsx"
    dados_xlsx = ler_xlsx_para_dicionario(caminho_arquivo)
    dados = []
    for linha in dados_xlsx:
        endereco = linha["Endereço"].split(",")

        if endereco[0] != " ":
            rua = endereco[0]
            bairro = endereco[2]

            if len(endereco) == 4:
                cidade_estado = endereco[3].split("-")
            else:
                cidade_estado = endereco[4].split("-")
                cep = re.sub("[^0-9]", "", endereco[3])

            cidade = cidade_estado[0]
            estado = cidade_estado[1] if len(cidade_estado) > 1 else ""

            num_casa = endereco[1].strip()

        telefone = linha["Telefone"].split(",")
        telefone = re.sub("[^0-9]", "", telefone[0])

        try:
            data_nascimento = datetime.datetime.strptime(
                str(linha["Data de Nascimento"]), "%d/%m/%Y"
            ).strftime("%Y-%m-%d")
        except:
            data_nascimento = datetime.datetime.strptime(
                str(linha["Data de Nascimento"]), "%Y-%m-%d %H:%M:%S"
            ).strftime("%Y-%m-%d")

        data_expedicao = dt.strptime(
            linha["Data de Matrícula"], "%d/%m/%Y %H:%M:%S"
        ).strftime("%Y-%m-%d")

        dict_to_append = {
            "tel": telefone,
            "cpf": re.sub("[^0-9]", "", linha["CPF"]),
            "nome": linha["Nome"],
            "data_nascimento": data_nascimento,
            "matricula": linha["Matrícula"],
            "expedicao_matricula": data_expedicao,
            "deficiencia": linha["Deficiência"].lower(),
        }

        if endereco[0] != " ":
            dict_to_append["endereco"] = {
                "logradouro": rua,
                "bairro": bairro,
                "cidade": cidade,
                "estado": estado,
                "cep": cep,
            }
        else:
            dict_to_append["endereco"] = ""

        if num_casa.isnumeric():
            dict_to_append["endereco"]["numero"] = endereco[1]

        elif (
            endereco != [" "] and
            (num_casa != "sn" or num_casa != "s/n")
        ):
            dict_to_append["endereco"]["numero"] = re.sub(
                "[^0-9]", "", endereco[1]
            )
            dict_to_append["endereco"]["complemento"] = re.sub(
                "[0-9]", "", endereco[1]
            )

        dados.append(dict_to_append)

    with transaction.atomic():
        from gerUsuarios.models import User, Tipo, Matricula, Contato, Deficiencia, Endereco

        for dado in dados:
            tipo = Tipo.objects.get(nome="Aluno".lower())

            try:
                deficiencia = Deficiencia.objects.get(
                    nome=dado["deficiencia"].lower()
                )
            except Deficiencia.DoesNotExist:
                deficiencia = None

            if dado["endereco"] != "":
                endereco = Endereco.objects.create(
                    logradouro=dado["endereco"]["logradouro"],
                    bairro=dado["endereco"]["bairro"],
                    cidade=dado["endereco"]["cidade"],
                    estado=dado["endereco"]["estado"],
                    cep=dado["endereco"]["cep"],
                    num_casa=dado["endereco"].get(
                        "numero"
                    ) if dado["endereco"].get("numero") else 0,
                    complemento=dado["endereco"].get("complemento", ""),
                )
            else:
                endereco = None

            if endereco:
                contato = Contato.objects.create(
                    endereco=endereco,
                    tel=dado["tel"],
                    email=f"caflo.{dado['matricula']}@aluno.ifpi.edu.br"
                )
            else:
                contato = None

            user, created = User.objects.get_or_create(
                cpf=dado["cpf"],
                defaults={
                    "nome": dado["nome"],
                    "data_nascimento": dado["data_nascimento"],
                    "password": make_password(dado["matricula"].lower()),
                    "tipo": tipo,
                    "email": f"caflo.{dado["matricula"]}@aluno.ifpi.edu.br",
                    "deficiencia": deficiencia,
                    "contato": contato,
                }
            )

            Matricula.objects.get_or_create(
                matricula=dado["matricula"],
                expedicao=dado["expedicao_matricula"],
                user=user,
            )

            user.save()


if __name__ == "__main__":
    main()
