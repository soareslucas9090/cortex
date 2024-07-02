from django.db import models


class Leitura(models.Model):
    corrente = models.FloatField(null=False)
    voltagem = models.FloatField(null=False)
    potencia = models.FloatField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        str = f"{self.potencia}"
