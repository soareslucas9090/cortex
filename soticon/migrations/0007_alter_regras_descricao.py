# Generated by Django 4.2.11 on 2024-09-26 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soticon', '0006_tickets_faltante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regras',
            name='descricao',
            field=models.CharField(max_length=512, unique=True),
        ),
    ]
