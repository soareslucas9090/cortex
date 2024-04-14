from django.contrib import admin

from .models import *


class UserSoticonAdmin(admin.ModelAdmin):
    pass


class StrikeAdmin(admin.ModelAdmin):
    pass


class JustificativaAdmin(admin.ModelAdmin):
    pass


class PosicaoFilaAdmin(admin.ModelAdmin):
    pass


class RotaAdmin(admin.ModelAdmin):
    pass


class TicketsAdmin(admin.ModelAdmin):
    pass


class RegrasAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserSoticon, UserSoticonAdmin)
admin.site.register(Strike, StrikeAdmin)
admin.site.register(Justificativa, JustificativaAdmin)
admin.site.register(PosicaoFila, PosicaoFilaAdmin)
admin.site.register(Rota, RotaAdmin)
admin.site.register(Tickets, TicketsAdmin)
admin.site.register(Regras, RegrasAdmin)
