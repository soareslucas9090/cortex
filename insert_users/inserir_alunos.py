import datetime
import re
from datetime import datetime as dt

import openpyxl
import requests

URL_BASE = "http://127.0.0.1:8000/"  # Troque caso esteja rodando em outro ip/porta
CPF = "12345678910"  # Aqui o CPF do ADMIN (somente números)
PASSWORD = "12345678"  # A senha do ADMIN


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


def authenticate_on_api(cpf, password):
    headers = {
        "Content-Type": "application/json",
    }
    data = {"cpf": cpf, "password": password}

    url = f"{URL_BASE}cortex/api/token/"

    response = requests.post(url, json=data, headers=headers)

    return response


def insert_data_on_api(access, data):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access}"}

    url = f"{URL_BASE}cortex/api/gerusuarios/v1/users/inserir_dados_completos/alunos/"

    response = requests.post(url, json=data, headers=headers)

    return response


def main():
    caminho_arquivo = "insert_users/usuarios.xlsx"
    dados_xlsx = ler_xlsx_para_dicionario(caminho_arquivo)
    data_json = []
    for linha in dados_xlsx:
        endereco = linha["Endereço"].split(",")

        rua = endereco[0]

        bairro = endereco[2]
        cep = re.sub("[^0-9]", "", endereco[3])

        cidade_estado = endereco[4].split("-")
        cidade = cidade_estado[0]
        estado = cidade_estado[1]

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

        data_validade = linha["Ano Letivo de Previsão de Conclusão"]
        data_validade = f"{data_validade}-12-30"
        data_expedicao = dt.strptime(
            linha["Data de Matrícula"], "%d/%m/%Y %H:%M:%S"
        ).strftime("%Y-%m-%d")

        dict_to_append = {
            "endereco": {
                "logradouro": rua,
                "bairro": bairro,
                "cidade": cidade,
                "estado": estado,
                "cep": cep,
            },
            "tel": telefone,
            "cpf": re.sub("[^0-9]", "", linha["CPF"]),
            "nome": linha["Nome"],
            "data_nascimento": data_nascimento,
            "matricula": linha["Matrícula"],
            "validade_matricula": data_validade,
            "expedicao_matricula": data_expedicao,
        }

        num_casa = endereco[1].strip()
        if num_casa.isnumeric():
            dict_to_append["endereco"]["numero"] = endereco[1]

        elif num_casa != "sn":
            dict_to_append["endereco"]["numero"] = re.sub("[^0-9]", "", endereco[1])
            dict_to_append["endereco"]["complemento"] = re.sub("[0-9]", "", endereco[1])

        data_json.append(dict_to_append)

    response = authenticate_on_api(CPF, PASSWORD)
    access = response.json()["access"]

    print(insert_data_on_api(access, data_json).json())


if __name__ == "__main__":
    main()
