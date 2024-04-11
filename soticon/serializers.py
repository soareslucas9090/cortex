from rest_framework import serializers

from .models import *


class UserSoticonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSoticon
        fields = "__all__"


class StrikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Strike
        fields = "__all__"


class JustificativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Justificativa
        fields = "__all__"


class PosicaoFilaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosicaoFila
        fields = "__all__"


class RotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rota
        fields = "__all__"


class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = "__all__"


class RegrasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regras
        fields = "__all__"
