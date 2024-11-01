from django.contrib.auth.hashers import make_password
from django.db import IntegrityError, transaction
from drf_spectacular.utils import OpenApiExample, OpenApiTypes, extend_schema_field
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


class PasswordResetRequestSerializer(serializers.Serializer):
    cpf = serializers.CharField(write_only=True)

    def validate_cpf(self, value):
        if len(value) != 11:
            raise serializers.ValidationError("CPF inválido.")

        return value


class PasswordResetCodeConfirmSerializer(serializers.Serializer):
    cpf = serializers.CharField(write_only=True)
    code = serializers.IntegerField(write_only=True)

    def validate_cpf(self, value):
        if len(value) != 11:
            raise serializers.ValidationError("CPF inválido.")

        return value

    def validate_code(self, value):
        if value < 1000 or value > 9999:
            raise serializers.ValidationError(
                "O código deve possuir 4 dígitos numéricos."
            )

        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    cpf = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate_cpf(self, value):
        if len(value) != 11:
            raise serializers.ValidationError("CPF inválido.")

        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "A senha precisa ter 8 caracteres ou mais."
            )

        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "nome",
            "email",
            "cpf",
            "deficiencia",
            "nome_deficiencia",
            "setores",
            "nome_setores",
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
    deficiencia = serializers.PrimaryKeyRelatedField(
        queryset=Deficiencia.objects.all(), write_only=True
    )
    setores = serializers.PrimaryKeyRelatedField(
        queryset=Setor.objects.all(), many=True, allow_empty=False, write_only=True
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

    nome_deficiencia = serializers.SerializerMethodField(read_only=True)
    nome_tipo = serializers.SerializerMethodField(read_only=True)
    nome_contato = serializers.SerializerMethodField(read_only=True)
    nome_empresa = serializers.SerializerMethodField(read_only=True)
    nome_setores = serializers.SerializerMethodField(read_only=True)
    matricula = serializers.SerializerMethodField()

    def get_nome_deficiencia(self, obj) -> str:
        try:
            deficiencia = Deficiencia.objects.get(id=obj.deficiencia.id).nome
            return deficiencia
        except:
            return None

    def get_nome_tipo(self, obj) -> str:
        try:
            nome = Tipo.objects.get(id=obj.tipo.id).nome
            return nome
        except:
            return None

    def get_nome_contato(self, obj) -> str:
        try:
            tel = Contato.objects.get(id=obj.contato.id).tel
            return tel
        except:
            return None

    def get_nome_empresa(self, obj) -> str:
        try:
            nome = Empresa.objects.get(id=obj.empresa.id).nome
            return nome
        except:
            return None

    @extend_schema_field(
        {
            "example": {"id": 0, "matricula": "example123", "is_ativo": True},
        }
    )
    def get_matricula(self, obj) -> dict | None:
        try:
            matriculas = Matricula.objects.filter(user=obj)
            serializer = Matricula2UserSerializer(matriculas, many=True)
            return serializer.data
        except:
            return None

    def get_nome_setores(self, obj) -> list[str]:
        try:
            setores = Setor_User.objects.filter(user=obj)
            data = []
            for setor in setores:
                data.append(setor.setor.nome)
            return data
        except:
            return None

    def validate_password(self, value):
        password = value

        if len(password) < 6:
            raise serializers.ValidationError("Must have at least 8 chars.")

        return password

    def validate_cpf(self, value):
        cpf = value

        if len(cpf) != 11:
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

    def validate_cep(self, value):
        if len(value) != 8:
            raise serializers.ValidationError("CEP Inválido.")

        return value

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
            raise serializers.ValidationError("Insira um estado válido (2 dígitos).")

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


class InserirAlunoCompletoSerializer(serializers.Serializer):
    endereco = EnderecoSerializer()
    email_externo = serializers.EmailField(required=False)
    tel = serializers.CharField(required=True)
    cpf = serializers.CharField(required=True)
    nome = serializers.CharField(required=True)
    data_nascimento = serializers.DateField(required=True)
    matricula = serializers.CharField(required=True)
    validade_matricula = serializers.DateField(required=True)
    expedicao_matricula = serializers.DateField(required=True)

    def create(self, validated_data):
        # Usar atomic para garantir que todos os dados sejam inseridos juntos
        with transaction.atomic():
            try:
                endereco_data = validated_data.pop("endereco", None)
                email_externo = validated_data.pop("email_externo", None)
                tel = validated_data.pop("tel", None)
                cpf = validated_data.pop("cpf", None)
                nome = validated_data.pop("nome", None)
                data_nascimento = validated_data.pop("data_nascimento", None)
                matricula_data = validated_data.pop("matricula", None)
                validade_matricula = validated_data.pop("validade_matricula", None)
                expedicao_matricula = validated_data.pop("expedicao_matricula", None)
            except Exception as e:
                raise serializers.ValidationError({"error": e})

            endereco = Endereco.objects.create(**endereco_data)
            contato = Contato.objects.create(
                endereco=endereco,
                email=email_externo,
                tel=tel,
            )

            email_user = f"caflo.{matricula_data}@aluno.ifpi.edu.br"
            password_user = make_password(f"{cpf[:6]}{matricula_data[-2:]}")
            tipo = Tipo.objects.get(nome__iexact="aluno")
            empresa = Empresa.objects.get(cnpj="10806496000491")
            setor = Setor.objects.get(nome__iexact="alunos")

            try:
                usuario = User.objects.create(
                    nome=nome,
                    cpf=cpf,
                    email=email_user,
                    tipo=tipo,
                    contato=contato,
                    empresa=empresa,
                    data_nascimento=data_nascimento,
                    password=password_user,
                )
            except IntegrityError as e:
                if "cpf" in str(e):
                    raise serializers.ValidationError(
                        {"cpf": f"Este CPF ({cpf}) já está cadastrado."}
                    )
                if "email" in str(e):
                    raise serializers.ValidationError(
                        {
                            "email": f"Um usuário com esta matrícula já foi registrado e possui um email ({email_user}) no sistema."
                        }
                    )

            usuario.setores.set([setor])

            try:
                matricula = Matricula.objects.create(
                    user=usuario,
                    matricula=matricula_data,
                    validade=validade_matricula,
                    expedicao=expedicao_matricula,
                )
            except IntegrityError as e:
                raise serializers.ValidationError(
                    {
                        "matricula": f"Um usuário com esta matrícula ({matricula_data}) já foi registrado no sistema."
                    }
                )

        return usuario

    def validate_cpf(self, value):
        if len(value) != 11 and not value.isnumeric():
            raise serializers.ValidationError("O CPF deve conter 11 dígitos numéricos.")

        return value

    def validate_tel(self, value):
        if len(value) != 11 and not value.isnumeric():
            raise serializers.ValidationError(
                "O telefone deve conter 11 dígitos numéricos."
            )

        return value


class InserirVariosAlunosCompletosSerializer(serializers.ListSerializer):
    def create(self, validated_data_list):
        users = []
        with transaction.atomic():
            for validated_data in validated_data_list:
                user = InserirAlunoCompletoSerializer().create(validated_data)
                users.append(user)
        return users


class InserirVariosAlunosCompletosWrapperSerializer(InserirAlunoCompletoSerializer):
    class Meta:
        list_serializer_class = InserirVariosAlunosCompletosSerializer


class InserirUsuarioCompletoSerializer(serializers.Serializer):
    endereco = EnderecoSerializer()
    email_externo = serializers.EmailField(required=False)
    email_institucional = serializers.EmailField(required=False)
    tel = serializers.CharField(required=True)
    cpf = serializers.CharField(required=True)
    nome = serializers.CharField(required=True)
    cnpj_empresa = serializers.CharField(required=True)
    tipo = serializers.CharField(required=True)
    setores = serializers.ListField(child=serializers.CharField(), required=False)
    data_nascimento = serializers.DateField(required=True)
    matricula = serializers.CharField(required=True)
    validade_matricula = serializers.DateField(required=True)
    expedicao_matricula = serializers.DateField(required=True)

    def create(self, validated_data):

        # Usar atomic para garantir que todos os dados sejam inseridos juntos
        with transaction.atomic():

            try:
                endereco_data = validated_data.pop("endereco")
                email_externo = validated_data.pop("email_externo", None)
                email_institucional = validated_data.pop("email_institucional", None)
                tel = validated_data.pop("tel")
                cpf = validated_data.pop("cpf")
                nome = validated_data.pop("nome")
                cnpj_empresa = validated_data.pop("cnpj_empresa")
                tipo_data = validated_data.pop("tipo")
                setores_data = validated_data.pop("setores", None)
                data_nascimento = validated_data.pop("data_nascimento")
                matricula_data = validated_data.pop("matricula")
                validade_matricula = validated_data.pop("validade_matricula")
                expedicao_matricula = validated_data.pop("expedicao_matricula")
            except Exception as e:
                raise serializers.ValidationError({"error": e})

            endereco = Endereco.objects.create(**endereco_data)
            contato = Contato.objects.create(
                endereco=endereco, email=email_externo, tel=tel
            )

            try:
                tipo = Tipo.objects.get(nome=tipo_data)
            except:
                raise serializers.ValidationError(
                    {"tipo": f"O tipo {tipo_data} não existe no sistema."}
                )

            try:
                setores = []

                for setor in setores_data:
                    setores.append(Setor.objects.get(nome__iexact=setor))

            except:
                raise serializers.ValidationError(
                    {"setores": f"Um dos setores passados não existe no sistema."}
                )

            try:
                empresa = Empresa.objects.get(cnpj=cnpj_empresa)
            except:
                raise serializers.ValidationError(
                    {
                        "empresa": f"A empresa de CNPJ {cnpj_empresa} não está cadastrada no sistema"
                    }
                )

            if not email_institucional:
                email_institucional = f"{matricula_data}@invalidemail.com"

            password_user = make_password(f"{cpf[:6]}{matricula_data[-2:]}")

            try:
                usuario = User.objects.create(
                    nome=nome,
                    cpf=cpf,
                    email=email_institucional,
                    tipo=tipo,
                    contato=contato,
                    empresa=empresa,
                    data_nascimento=data_nascimento,
                    password=password_user,
                )
            except IntegrityError as e:
                if "cpf" in str(e):
                    raise serializers.ValidationError(
                        {"cpf": f"Este CPF ({cpf}) já está cadastrado."}
                    )
                if "email" in str(e):
                    raise serializers.ValidationError(
                        {
                            "email": f"Um usuário com esta matrícula já foi registrado e possui um email ({email_institucional}) no sistema."
                        }
                    )

            usuario.setores.set(setores)

            try:
                matricula = Matricula.objects.create(
                    user=usuario,
                    matricula=matricula_data,
                    validade=validade_matricula,
                    expedicao=expedicao_matricula,
                )
            except IntegrityError as e:
                raise serializers.ValidationError(
                    {
                        "matricula": f"Um usuário com esta matrícula ({matricula_data}) já foi registrado no sistema."
                    }
                )

        return usuario

    def validate_cpf(self, value):
        if len(value) != 11 and not value.isnumeric():
            raise serializers.ValidationError("O CPF deve conter 11 dígitos numéricos.")

        return value

    def validate_tel(self, value):
        if len(value) != 11 and not value.isnumeric():
            raise serializers.ValidationError(
                "O telefone deve conter 11 dígitos numéricos."
            )

        return value

    def validate_cnpj(self, value):
        if len(value) != 14 and not value.isnumeric():
            raise serializers.ValidationError(
                "O CNPJ deve conter 14 dígitos numéricos."
            )

        return value


class InserirVariosUsuariosCompletosSerializer(serializers.ListSerializer):
    def create(self, validated_data_list):
        users = []
        with transaction.atomic():
            for validated_data in validated_data_list:
                user = InserirUsuarioCompletoSerializer().create(validated_data)
                users.append(user)
        return users


class InserirVariosUsuariosCompletosWrapperSerializer(InserirUsuarioCompletoSerializer):
    class Meta:
        list_serializer_class = InserirVariosUsuariosCompletosSerializer


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


class DeficienciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deficiencia
        fields = "__all__"
