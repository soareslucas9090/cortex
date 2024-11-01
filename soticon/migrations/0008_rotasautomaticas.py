# Generated by Django 4.2.11 on 2024-10-13 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soticon', '0007_alter_regras_descricao'),
    ]

    operations = [
        migrations.CreateModel(
            name='RotasAutomaticas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horario', models.TimeField()),
                ('dia_da_semana', models.CharField(choices=[('segunda', 'Segunda-feira'), ('terca', 'Terça-feira'), ('quarta', 'Quarta-feira'), ('quinta', 'Quinta-feira'), ('sexta', 'Sexta-feira'), ('sabado', 'Sábado'), ('domingo', 'Domingo')], max_length=10)),
            ],
        ),
    ]