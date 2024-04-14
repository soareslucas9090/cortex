from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    pass


class EnderecoAdmin(admin.ModelAdmin):
    pass


class TipoAdmin(admin.ModelAdmin):
    pass


class ContatoAdmin(admin.ModelAdmin):
    pass


class EmpresaAdmin(admin.ModelAdmin):
    pass


class SetorAdmin(admin.ModelAdmin):
    pass


class SetorUserAdmin(admin.ModelAdmin):
    pass


class TipoMatriculaAdmin(admin.ModelAdmin):
    pass


class MatriculaAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(Tipo, TipoAdmin)
admin.site.register(Contato, ContatoAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Setor, SetorAdmin)
admin.site.register(Setor_User, SetorUserAdmin)
admin.site.register(Tipo_Matricula, TipoMatriculaAdmin)
admin.site.register(Matricula, MatriculaAdmin)
