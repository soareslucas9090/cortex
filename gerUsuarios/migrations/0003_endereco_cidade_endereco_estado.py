# Generated by Django 4.2.11 on 2024-04-28 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerUsuarios', '0002_alter_user_contato_alter_user_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='endereco',
            name='cidade',
            field=models.CharField(default='floriano', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='endereco',
            name='estado',
            field=models.CharField(default='pi', max_length=2),
            preserve_default=False,
        ),
    ]
