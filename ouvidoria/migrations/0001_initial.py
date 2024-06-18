# Generated by Django 4.2.11 on 2024-06-10 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bloco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=255)),
                ('isativo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reclamacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_reclamacao', models.DateTimeField()),
                ('descricao_reclamacao', models.TextField()),
                ('titulo', models.CharField(max_length=300)),
                ('lida', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='StatusReclamacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=255)),
                ('isativo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoReclamacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=255)),
                ('isativo', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='tiporeclamacao',
            constraint=models.UniqueConstraint(fields=('descricao', 'isativo'), name='unique_descricao_constraint'),
        ),
        migrations.AddConstraint(
            model_name='statusreclamacao',
            constraint=models.UniqueConstraint(fields=('descricao', 'isativo'), name='unique_status_constraint'),
        ),
        migrations.AddField(
            model_name='reclamacao',
            name='bloco',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='ouvidoria.bloco'),
        ),
        migrations.AddField(
            model_name='reclamacao',
            name='status_reclamacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='ouvidoria.statusreclamacao'),
        ),
        migrations.AddField(
            model_name='reclamacao',
            name='tipo_reclamacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='ouvidoria.tiporeclamacao'),
        ),
        migrations.AddField(
            model_name='reclamacao',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_ouvidoria', to=settings.AUTH_USER_MODEL),
        ),
    ]