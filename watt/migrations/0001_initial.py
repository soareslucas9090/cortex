# Generated by Django 4.2.11 on 2024-07-02 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Leitura",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("corrente", models.FloatField()),
                ("voltagem", models.FloatField()),
                ("potencia", models.FloatField()),
            ],
        ),
    ]
