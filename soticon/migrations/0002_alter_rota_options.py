# Generated by Django 4.2.11 on 2024-04-23 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('soticon', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rota',
            options={'ordering': ['-data']},
        ),
    ]