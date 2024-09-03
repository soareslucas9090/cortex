from rest_framework import serializers

from .models import *


class User2AdminSerializer(serializers.ModelSerializer):
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "nome",
            "email",
            "cpf",
            "setores",
            "tipo",
            "nome_tipo",
            "contato",
            "nome_contato",
            "empresa",
            "nome_empresa",
            "matricula",
            "data_nascimento",
            "password",
        ]

    password = serializers.CharField(write_only=True)
    setores = serializers.PrimaryKeyRelatedField(
        queryset=Setor.objects.all(), many=True, allow_empty=False
    )

    tipo = serializers.PrimaryKeyRelatedField(
        queryset=Tipo.objects.all(), write_only=True
    )
    contato = serializers.PrimaryKeyRelatedField(
        queryset=Contato.objects.all(), allow_empty=False, write_only=True
    )
    empresa = serializers.PrimaryKeyRelatedField(
        queryset=Empresa.objects.all(), allow_empty=False, write_only=True
    )

    nome_tipo = serializers.SerializerMethodField(read_only=True)
    nome_contato = serializers.SerializerMethodField(read_only=True)
    nome_empresa = serializers.SerializerMethodField(read_only=True)
    matricula = serializers.SerializerMethodField()

    def get_nome_tipo(self, obj):
        try:
            nome = Tipo.objects.get(id=obj.tipo.id).nome
            return nome
        except:
            return None

    def get_nome_contato(self, obj):
        try:
            tel = Contato.objects.get(id=obj.contato.id).tel
            return tel
        except:
            return None

    def get_nome_empresa(self, obj):
        try:
            nome = Empresa.objects.get(id=obj.empresa.id).nome
            return nome
        except:
            return None

    def get_matricula(self, obj):
        try:
            matriculas = Matricula.objects.filter(user=obj)
            serializer = Matricula2UserSerializer(matriculas, many=True)
            return serializer.data
        except:
            return None

    def validate_password(self, value):
        password = value

        if len(password) < 6:
            raise serializers.ValidationError("Must have at least 8 chars.")

        return password

    def validate_cpf(self, value):
        cpf = value

        if len(cpf) < 11:
            raise serializers.ValidationError("Must have at least 11 chars.")

        return cpf


class TipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo
        fields = "__all__"


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = "__all__"

    def validate_estado(self, value):
        estados = [
            "ac",
            "al",
            "ap",
            "am",
            "ba",
            "ce",
            "df",
            "es",
            "go",
            "ma",
            "mt",
            "ms",
            "mg",
            "pa",
            "pb",
            "pr",
            "pe",
            "pi",
            "rj",
            "rn",
            "rs",
            "ro",
            "rr",
            "sc",
            "sp",
            "se",
            "to",
        ]

        estado = value.lower()

        if estado not in estados:
            raise serializers.ValidationError("Insira um estado válido")

        return estado


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


class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = "__all__"

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


class Matricula2UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = [
            "id",
            "matricula",
            "is_ativo",
        ]
