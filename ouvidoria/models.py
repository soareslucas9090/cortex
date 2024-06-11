from django.db import models

from gerUsuarios import models as modelsUsusarios


class StatusReclamacao(models.Model):
    descricao = models.CharField(max_length=255, null=False)
    isativo = models.BooleanField(default=True, null=False)

    def __str__(self):
        str = f"{self.descricao}"
        return str

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["descricao", "isativo"], name="unique_status_constraint"
            )
        ]


class TipoReclamacao(models.Model):
    descricao = models.CharField(max_length=255, null=False)
    isativo = models.BooleanField(default=True, null=False)

    def __str__(self):
        str = f"{self.descricao}"
        return str

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["descricao", "isativo"], name="unique_descricao_constraint"
            )
        ]


class Bloco(models.Model):
    descricao = models.CharField(max_length=255, null=False)
    isativo = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f"{self.descricao}"


class Reclamacao(models.Model):
    data_reclamacao = models.DateTimeField(null=False)
    descricao_reclamacao = models.TextField(null=False)
    titulo = models.CharField(max_length=300, null=False)
    lida = models.BooleanField(default=False, null=False)
    status_reclamacao = models.ForeignKey(
        StatusReclamacao, on_delete=models.RESTRICT, null=False
    )
    tipo_reclamacao = models.ForeignKey(
        TipoReclamacao, on_delete=models.RESTRICT, null=False
    )
    bloco = models.ForeignKey(Bloco, on_delete=models.RESTRICT, null=False)
    usuario = models.OneToOneField(
        modelsUsusarios.User,
        related_name="user_ouvidoria",
        on_delete=models.CASCADE,
        null=False,
    )

    def __str__(self):
        return f"{self.titulo} - {self.data_reclamacao}"
