# Generated by Django 4.2.11 on 2024-05-01 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soticon', '0003_alter_rota_horario'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tickets',
            options={'ordering': ['rota']},
        ),
    ]
