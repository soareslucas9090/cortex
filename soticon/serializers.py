from rest_framework import serializers

from gerUsuarios.models import User

from .models import *


class UserSoticonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSoticon
        fields = "__all__"

    nome = serializers.SerializerMethodField()
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def get_nome(self, obj):
        nome = User.objects.get(id=obj.usuario.id).nome
        return nome


class StrikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Strike
        fields = "__all__"

    user_soticon = serializers.PrimaryKeyRelatedField(
        queryset=UserSoticon.objects.all()
    )
    nome = serializers.SerializerMethodField()

    def get_nome(self, obj):
        nome = User.objects.get(id=obj.usuario.id).nome
        return nome


class JustificativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Justificativa
        fields = "__all__"

    strike = serializers.PrimaryKeyRelatedField(queryset=Strike.objects.all())


class PosicaoFilaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosicaoFila
        fields = "__all__"


class RotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rota
        fields = "__all__"

    def validate_status(self, value):
        status = value
        status_aceitos = ["espera", "cancelada", "executada"]

        if not (status.lower() in status_aceitos):
            status_aceitos_str = ", ".join(status_aceitos)
            raise serializers.ValidationError(
                f"O status deve ser um dos seguintes: {status_aceitos_str}"
            )

        return status.lower()


class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = "__all__"

    nome = serializers.SerializerMethodField()
    cpf = serializers.SerializerMethodField()

    def get_nome(self, obj):
        nome = User.objects.get(id=obj.user_soticon.id).nome
        return nome

    def get_cpf(self, obj):
        cpf = User.objects.get(id=obj.user_soticon.id).cpf
        return cpf

    rota = serializers.PrimaryKeyRelatedField(queryset=Rota.objects.all())
    user_soticon = serializers.PrimaryKeyRelatedField(
        queryset=UserSoticon.objects.all()
    )
    posicao_fila = serializers.PrimaryKeyRelatedField(
        queryset=PosicaoFila.objects.all(), required=False, allow_null=True
    )

    def validate(self, data):
        if "user_soticon" not in data or "rota" not in data:
            raise serializers.ValidationError(
                "É obrigatório informar o id do usuário e da rota!"
            )

        return data


class SoticonTicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = "__all__"


class RegrasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regras
        fields = "__all__"


class ReservarTicketSerializer(serializers.Serializer):
    rota = serializers.IntegerField()
