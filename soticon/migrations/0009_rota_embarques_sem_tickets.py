# Generated by Django 4.2.11 on 2024-11-04 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soticon', '0008_rotasautomaticas'),
    ]

    operations = [
        migrations.AddField(
            model_name='rota',
            name='embarques_sem_tickets',
            field=models.IntegerField(null=True),
        ),
    ]