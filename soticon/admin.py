from django.contrib import admin

from gerUsuarios.admin import admin_custom_site

from .models import *


class UserSoticonAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "faltas")
    search_fields = ("usuario",)
    ordering = ("usuario",)


class RegrasSoticonAdmin(admin.ModelAdmin):
    list_display = ("descricao", "parametro")
    search_fields = ("descricao",)
    ordering = ("descricao",)


admin_custom_site.register(UserSoticon, UserSoticonAdmin)
admin_custom_site.register(Regras, RegrasSoticonAdmin)
