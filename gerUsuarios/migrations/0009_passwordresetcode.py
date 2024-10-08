# Generated by Django 4.2.11 on 2024-09-12 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gerUsuarios', '0008_alter_empresa_contato'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordResetCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expiration_time', models.DateTimeField()),
                ('code', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
