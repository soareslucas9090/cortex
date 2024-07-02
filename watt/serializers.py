from rest_framework import serializers

from .models import *


class LeituraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leitura
        fields = [
            "corrente",
            "voltagem",
            "potencia",
        ]
