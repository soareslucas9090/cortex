# Generated by Django 4.2.11 on 2024-09-15 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gerUsuarios', '0015_alter_contato_endereco_alter_empresa_contato_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='contato',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='usuario_contato', to='gerUsuarios.contato'),
        ),
    ]
