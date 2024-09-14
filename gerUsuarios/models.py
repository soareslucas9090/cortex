from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Permission,
    PermissionsMixin,
    User,
)
from django.db import models
from django.utils import timezone


class Base(models.Model):
    is_ativo = models.BooleanField(default=True, null=False)

    class Meta:
        abstract = True


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
    cidade = models.CharField(max_length=60, null=False)
    estado = models.CharField(max_length=2, null=False)
    bairro = models.CharField(max_length=30, null=False)
    cep = models.CharField(max_length=8, null=True)
    complemento = models.CharField(max_length=30, null=True)
    num_casa = models.IntegerField(null=True)

    def __str__(self):
        str = f"{self.logradouro}"
        return str

    def save(self, *args, **kwargs):
        self.cidade = self.cidade.lower()
        self.bairro = self.bairro.lower()
        if self.complemento:
            self.complemento = self.complemento.lower()
        self.logradouro = self.logradouro.lower()
        super().save(*args, **kwargs)


class Contato(Base):
    endereco = models.ForeignKey(
        Endereco,
        related_name="contato_associado",
        on_delete=models.RESTRICT,
        null=False,
    )
    email = models.EmailField(max_length=60, null=True)
    tel = models.CharField(max_length=11, null=False)

    def __str__(self):
        str = f"{self.email}"
        return str

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)


class Empresa(Base):
    contato = models.ForeignKey(
        Contato, related_name="empresa_associada", on_delete=models.RESTRICT, null=True
    )
    nome = models.CharField(max_length=30, null=False, unique=True)
    cnpj = models.CharField(max_length=14, unique=True, null=False)

    def __str__(self):
        str = f"{self.nome}"
        return str


class UserManager(BaseUserManager):
    def create_user(
        self,
        cpf,
        nome,
        email,
        tipo,
        data_nascimento,
        password=None,
        **extra_fields,
    ):
        if not nome:
            raise ValueError("O usuário precisa de um nome válido!")
        if not cpf:
            raise ValueError("O usuário precisa fornecer um CPF válido!")
        if not email:
            raise ValueError("O usuário precisa fornecer um email válido!")
        if not tipo:
            raise ValueError("O usuário precisa fornecer um tipo válido!")
        if not data_nascimento:
            raise ValueError(
                "O usuário precisa fornecer uma data de nascimento válida!"
            )

        user = self.model(
            cpf=cpf,
            nome=nome,
            email=self.normalize_email(email),
            tipo=Tipo.objects.get(pk=tipo),
            data_nascimento=data_nascimento,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        cpf,
        nome,
        email,
        tipo,
        data_nascimento,
        password=None,
        **extra_fields,
    ):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.create_user(
            cpf=cpf,
            nome=nome,
            email=email,
            tipo=tipo,
            data_nascimento=data_nascimento,
            password=password,
            **extra_fields,
        )

        permissions = Permission.objects.all()
        user.user_permissions.set(permissions)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    tipo = models.ForeignKey(
        Tipo, related_name="usuarios_tipo", on_delete=models.RESTRICT, null=False
    )
    contato = models.ForeignKey(
        Contato, related_name="usuario_contato", on_delete=models.RESTRICT, null=True
    )
    empresa = models.ForeignKey(
        Empresa, related_name="usuarios_empresa", on_delete=models.RESTRICT, null=True
    )
    cpf = models.CharField(max_length=11, null=False, unique=True)
    data_nascimento = models.DateField(null=True)
    setores = models.ManyToManyField("Setor", through="Setor_User")

    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = [
        "nome",
        "email",
        "tipo",
        "data_nascimento",
    ]

    USERNAME_FIELD = "cpf"

    objects = UserManager()

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        self.nome = self.nome.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


class PasswordResetCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(null=False)
    code = models.IntegerField(null=False)
    validated = models.BooleanField(default=False)

    def __str__(self):
        return f"User {self.user}, code {self.code}"

    def is_expired(self):
        return self.expiration_time < timezone.now()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "code"], name="unique_code_user_constraint"
            )
        ]


class Setor(Base):
    nome = models.CharField(max_length=50, null=False, unique=True)

    def save(self, *args, **kwargs):
        self.nome = self.nome.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        str = f"{self.nome}"
        return str


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


class Matricula(Base):
    user = models.ForeignKey(
        User, related_name="matricula", on_delete=models.RESTRICT, null=False
    )
    matricula = models.CharField(max_length=19, null=False, unique=True)
    validade = models.DateField(null=True)
    expedicao = models.DateField(null=False)

    def __str__(self):
        str = f"{self.matricula}"
        return str
