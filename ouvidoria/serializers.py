from rest_framework import serializers

from gerUsuarios.models import User

from .models import *


class StatusReclamacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusReclamacao
        fields = "__all__"


class TipoReclamacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoReclamacao
        fields = "__all__"


class BlocoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bloco
        fields = "__all__"


class ReclamacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reclamacao
        fields = "__all__"

    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    status_reclamacao = serializers.PrimaryKeyRelatedField(
        queryset=StatusReclamacao.objects.all()
    )
    tipo_reclamacao = serializers.PrimaryKeyRelatedField(
        queryset=TipoReclamacao.objects.all()
    )
    bloco = serializers.PrimaryKeyRelatedField(queryset=Bloco.objects.all())
    nomeUsurio = serializers.SerializerMethodField()

    def get_nome(self, obj):
        nome = User.objects.get(id=obj.usuario.id).nome
        return nome
