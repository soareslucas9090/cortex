from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    password = serializers.CharField(write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    setores = serializers.PrimaryKeyRelatedField(
        queryset=Setor.objects.all(), many=True, allow_empty=False
    )
    tipo = serializers.PrimaryKeyRelatedField(queryset=Tipo.objects.all())
    contato = serializers.PrimaryKeyRelatedField(
        queryset=Contato.objects.all(), allow_empty=False
    )
    empresa = serializers.PrimaryKeyRelatedField(
        queryset=Empresa.objects.all(), allow_empty=False
    )
    matricula = serializers.SerializerMethodField()

    def validate_password(self, value):
        password = value

        if len(password) < 6:
            raise serializers.ValidationError("Must have at least 8 chars.")

        return password

    def get_matricula(self, obj):
        try:
            matriculas = Matricula.objects.filter(user=obj)
            serializer = Matricula2UserSerializer(matriculas, many=True)
            return serializer.data
        except:
            return None


class TipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo
        fields = "__all__"


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = "__all__"


class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contato
        fields = "__all__"

    endereco = serializers.PrimaryKeyRelatedField(queryset=Endereco.objects.all())


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = "__all__"

    contato = serializers.PrimaryKeyRelatedField(queryset=Contato.objects.all())


class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = "__all__"


class Setor_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor_User
        fields = "__all__"

    setor = serializers.PrimaryKeyRelatedField(queryset=Setor.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


"""
class Alteracao_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alteracao_User
        fields = "__all__"

        user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
"""


class Tipo_MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Matricula
        fields = "__all__"


class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = "__all__"

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    tipo_matricula = serializers.PrimaryKeyRelatedField(
        queryset=Tipo_Matricula.objects.all()
    )


class Matricula2UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = [
            "id",
            "matricula",
            "tipo_matricula",
            "is_ativo",
        ]

    tipo_matricula = serializers.PrimaryKeyRelatedField(
        queryset=Tipo_Matricula.objects.all()
    )
