from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.db import models


class Base(models.Model):
    is_ativo = models.BooleanField(default=True, null=False)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(
        self,
        nome,
        cpf,
        password=None,
    ):
        if not nome:
            raise ValueError("O usuário precisa de um nome válido")
        if not cpf:
            raise ValueError("O usuário precisa fornecer um CPF válido")

        user = self.model(
            nome=nome,
            cpf=cpf,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        nome,
        cpf,
        password,
    ):
        user = self.create_user(
            nome=nome,
            cpf=cpf,
            password=password,
        )

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    nome = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    tipo = models.ForeignKey(
        "Tipo", related_name="user_tipo", on_delete=models.RESTRICT, null=False
    )
    contato = models.ForeignKey(
        "Contato", related_name="user_contato", on_delete=models.RESTRICT, null=False
    )
    empresa = models.ForeignKey(
        "Empresa", related_name="user_empresa", on_delete=models.RESTRICT, null=False
    )
    cpf = models.CharField(max_length=11, null=False, unique=True)
    data_nascimento = models.DateField(null=False)
    setores = models.ManyToManyField("Setor", through="Setor_User")

    date_joined = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = [
        "name",
    ]

    USERNAME_FIELD = "cpf"

    objects = UserManager()

    def __str__(self):
        str = f"{self.nome}"
        return str

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


class Tipo(Base):
    nome = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        str = f"{self.nome}"
        return str

    def save(self, *args, **kwargs):
        self.nome = self.nome.lower()
        super().save(*args, **kwargs)


class Endereco(Base):
    logradouro = models.CharField(max_length=60, null=False)
    bairro = models.CharField(max_length=30, null=False)
    cep = models.CharField(max_length=8, null=False)
    complemento = models.CharField(max_length=30, null=True)
    num_casa = models.IntegerField(null=False)


class Contato(Base):
    endereco = models.ForeignKey(
        Endereco, related_name="contato_endereco", on_delete=models.RESTRICT, null=False
    )
    email = models.EmailField(max_length=60, null=False)
    tel = models.CharField(max_length=11, null=False)


class Empresa(Base):
    contato = models.ForeignKey(
        Contato, related_name="empresa_contato", on_delete=models.RESTRICT, null=False
    )
    nome = models.CharField(max_length=30, null=False)
    cnpj = models.CharField(max_length=14, unique=True, null=False)


class Setor(Base):
    nome = models.CharField(max_length=50, null=False)

    def save(self, *args, **kwargs):
        self.nome = self.nome.lower()
        super().save(*args, **kwargs)


class Setor_User(Base):
    setor = models.ForeignKey(
        Setor, related_name="setor_user_setor", on_delete=models.CASCADE, null=False
    )
    user = models.ForeignKey(
        User, related_name="setor_user_user", on_delete=models.CASCADE, null=False
    )

    def __str__(self):
        str = f"Setor: {self.setor} e Usuario: {self.usuario}"
        return str


"""
class Alteracao_User(models.Model):
    user = models.ForeignKey(
        User, related_name="alteracao_user_user", on_delete=models.RESTRICT, null=False
    )
    analisado = models.BooleanField(default=False, null=False)
    aprovado = models.BooleanField(default=False, null=False)
    antigo_contato = models.IntegerField(null=True)
    novo_contato = models.IntegerField(null=True)
    user_analista = models.IntegerField(null=True)
"""


class Tipo_Matricula(Base):
    descricao = models.CharField(max_length=60, null=False)

    def save(self, *args, **kwargs):
        self.descricao = self.descricao.lower()
        super().save(*args, **kwargs)


class Matricula(Base):
    user = models.ForeignKey(
        User, related_name="matricula_user", on_delete=models.RESTRICT, null=False
    )
    tipo_matricula = models.ForeignKey(
        Tipo_Matricula,
        related_name="tipo_matricula",
        on_delete=models.RESTRICT,
        null=False,
    )
    matricula = models.CharField(max_length=19, null=False, unique=True)
    validade = models.DateField(null=True)
    expedicao = models.DateField(null=False)
