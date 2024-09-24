from typing import Any

from django.contrib import admin

from .forms import *
from .models import *


# Classe feita para permitir acesso ao painel admin apenas a usuários super_user
class CustomAdminSite(admin.AdminSite):
    site_header = "Painel Admin - CORTEX/SOTICON"
    site_title = "Cortex Admin"
    index_title = "Bem-vindo ao Painel Admin - CORTEX/SOTICON"

    def has_permission(self, request):
        return request.user.is_superuser


admin_custom_site = CustomAdminSite(name="custom_admin")


# Classe responsável por exibir um Inline de Matrícula dentro da edição do usuário
class MatriculaInline(admin.TabularInline):
    model = Matricula
    extra = 0


# Classe responsável por exibir um Inline de Setores dentro da edição do usuário
class SetorUserInline(admin.TabularInline):
    model = Setor_User
    extra = 0


class UserAdmin(admin.ModelAdmin):
    form = AdminPortalUserForm

    # Ações customizadas
    actions = ["make_active", "make_inactive"]

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_active.short_description = "Marcar usuários selecionados como ativos"
    make_inactive.short_description = "Marcar usuários selecionados como inativos"

    # Filtra contatos que não têm um usuário associado
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "contato":
            kwargs["queryset"] = Contato.objects.filter(usuario_contato__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Torna o campo contato somente leitura para usuários que já possuem um contato registrado
    # Ainda é possível editar o contato clicando no nome dele
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.contato:
            return ["contato"]
        return []

    list_display = (
        "cpf",
        "id",
        "nome",
        "email",
        "tipo",
        "data_nascimento",
        "is_active",
        "is_superuser",
        "date_joined",
    )
    list_filter = ("is_active", "tipo", "is_superuser")
    inlines = [MatriculaInline, SetorUserInline]

    # Divisão dos itens para edição em Categorias
    fieldsets = [
        ("Credenciais", {"fields": ["cpf", "password"]}),
        (
            "Iformações pessoais",
            {
                "fields": (
                    "nome",
                    "data_nascimento",
                    "email",
                    "contato",
                    "empresa",
                )
            },
        ),
        ("Permissões", {"fields": ("tipo", "is_superuser")}),
    ]

    # Fieldsets para criação
    add_fieldsets = [
        (
            "Credenciais",
            {
                "classes": ["wide"],
                "fields": [
                    "cpf",
                    "password",
                ],
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "nome",
                    "data_nascimento",
                    "email",
                    "contato",
                    "empresa",
                )
            },
        ),
        ("Permissions", {"fields": ("tipo", "is_superuser")}),
    ]

    search_fields = ("cpf", "nome")
    ordering = ("nome",)


class EnderecoAdmin(admin.ModelAdmin):
    pass


class TipoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "is_ativo")
    search_fields = ("nome",)
    list_filter = ("is_ativo",)
    ordering = ("nome",)


class ContatoAdmin(admin.ModelAdmin):
    pass


class EmpresaAdmin(admin.ModelAdmin):
    search_fields = (
        "id",
        "nome",
    )
    list_filter = ("is_ativo",)
    ordering = ("nome",)


class SetorAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "is_ativo")
    search_fields = ("nome",)
    list_filter = ("is_ativo",)
    ordering = ("nome",)


class MatriculaAdmin(admin.ModelAdmin):
    list_display = ("id", "matricula", "user", "is_ativo")
    search_fields = ("matricula", "user__nome")
    list_filter = ("is_ativo", "user")
    ordering = ("matricula",)


admin_custom_site.register(User, UserAdmin)
admin_custom_site.register(Endereco, EnderecoAdmin)
admin_custom_site.register(Tipo, TipoAdmin)
admin_custom_site.register(Contato, ContatoAdmin)
admin_custom_site.register(Empresa, EmpresaAdmin)
admin_custom_site.register(Setor, SetorAdmin)
admin_custom_site.register(Matricula, MatriculaAdmin)
