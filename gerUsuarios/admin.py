from django.contrib import admin

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome",
        "email",
        "tipo",
        "contato",
        "empresa",
        "cpf",
        "data_nascimento",
        "is_ativo",
    )


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "logradouro",
        "bairro",
        "cep",
        "complemento",
        "num_casa",
        "is_ativo",
    )


@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "is_ativo")


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ("id", "endereco", "email", "tel", "is_ativo")


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("id", "contato", "nome", "cnpj", "is_ativo")
