# Generated by Django 4.2.11 on 2024-04-27 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soticon', '0002_alter_rota_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rota',
            name='horario',
            field=models.TimeField(),
        ),
    ]
