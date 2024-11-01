from rest_framework import serializers

from gerUsuarios.models import User

from .models import *


class UserSoticonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSoticon
        fields = "__all__"

    nome = serializers.SerializerMethodField()
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def get_nome(self, obj) -> str:
        nome = User.objects.get(id=obj.usuario.id).nome
        return nome


class StrikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Strike
        fields = "__all__"

    user_soticon = serializers.PrimaryKeyRelatedField(
        queryset=UserSoticon.objects.select_related("usuario").all()
    )
    nome = serializers.SerializerMethodField()

    def get_nome(self, obj) -> str:
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

    rota = serializers.PrimaryKeyRelatedField(queryset=Rota.objects.all())
    user_soticon = serializers.PrimaryKeyRelatedField(
        queryset=UserSoticon.objects.select_related("usuario").all()
    )
    posicao_fila = serializers.PrimaryKeyRelatedField(
        queryset=PosicaoFila.objects.all(), required=False, allow_null=True
    )


class TicketsDetalhadosParaVerificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = "__all__"

    nome = serializers.SerializerMethodField()
    cpf = serializers.SerializerMethodField()
    deficiencia = serializers.SerializerMethodField()
    usuario = None
    obj_test = None

    def get_deficiencia(self, obj):
        if self.usuario:
            if self.obj_test != obj:
                self.obj_test = obj
                self.usuario = User.objects.get(id=obj.user_soticon.usuario.id)
                if self.usuario.deficiencia:
                    deficiencia = self.usuario.deficiencia.nome
                    return deficiencia
                else:
                    return None
            else:
                if self.usuario.deficiencia:
                    deficiencia = self.usuario.deficiencia.nome
                    return deficiencia
                else:
                    return None
        else:
            self.obj_test = obj
            self.usuario = User.objects.get(id=obj.user_soticon.usuario.id)
            if self.usuario.deficiencia:
                deficiencia = self.usuario.deficiencia.nome
                return deficiencia
            else:
                return None

    def get_nome(self, obj):
        if self.usuario:
            if self.obj_test != obj:
                self.obj_test = obj
                self.usuario = User.objects.get(id=obj.user_soticon.usuario.id)
                nome = self.usuario.nome
                return nome
            else:
                return self.usuario.nome
        else:
            self.obj_test = obj
            self.usuario = User.objects.get(id=obj.user_soticon.usuario.id)
            nome = self.usuario.nome
            return nome

    def get_cpf(self, obj):
        if self.usuario:
            if self.obj_test != obj:
                self.obj_test = obj
                self.usuario = User.objects.get(id=obj.user_soticon.usuario.id)
                cpf = self.usuario.cpf
                return cpf
            else:
                return self.usuario.cpf
        else:
            self.obj_test = obj
            self.usuario = User.objects.get(id=obj.user_soticon.usuario.id)
            cpf = self.usuario.cpf
            return cpf

    rota = serializers.PrimaryKeyRelatedField(queryset=Rota.objects.all())
    user_soticon = serializers.PrimaryKeyRelatedField(
        queryset=UserSoticon.objects.select_related("usuario").all()
    )
    posicao_fila = serializers.PrimaryKeyRelatedField(
        queryset=PosicaoFila.objects.all(), required=False, allow_null=True
    )


class TicketsDetalhadosParaDetalhesUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = ["posicao_fila", "data", "horario"]

    posicao_fila = serializers.PrimaryKeyRelatedField(
        queryset=PosicaoFila.objects.all()
    )

    data = serializers.SerializerMethodField()
    horario = serializers.SerializerMethodField()

    def get_data(self, obj):
        return obj.rota.data

    def get_horario(self, obj):
        return obj.rota.horario


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


class FinalizarRotaSerializer(serializers.Serializer):
    status = serializers.CharField(required=True)
    obs = serializers.CharField(required=False)


class RotasAutomaticasSerializer(serializers.ModelSerializer):
    class Meta:
        model = RotasAutomaticas
        fields = "__all__"
