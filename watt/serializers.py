from rest_framework import serializers

from .models import *


class LeituraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leitura
        fields = ["corrente", "voltagem", "potencia", "valor_consumo"]

    valor_consumo = serializers.SerializerMethodField(read_only=True)

    def get_valor_consumo(self, obj):
        return 0.853 * (obj.potencia / 1000)
