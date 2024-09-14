# Generated by Django 4.2.11 on 2024-09-14 22:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gerUsuarios', '0014_alter_contato_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contato',
            name='endereco',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='contato_associado', to='gerUsuarios.endereco'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='contato',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='empresa_associada', to='gerUsuarios.contato'),
        ),
        migrations.AlterField(
            model_name='matricula',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='matricula', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='contato',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='usuario_contato', to='gerUsuarios.contato'),
        ),
        migrations.AlterField(
            model_name='user',
            name='empresa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='usuarios_empresa', to='gerUsuarios.empresa'),
        ),
        migrations.AlterField(
            model_name='user',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='usuarios_tipo', to='gerUsuarios.tipo'),
        ),
    ]
