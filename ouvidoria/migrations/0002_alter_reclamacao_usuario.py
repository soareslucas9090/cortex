# Generated by Django 4.2.11 on 2024-06-18 04:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ouvidoria', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reclamacao',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_ouvidoria', to=settings.AUTH_USER_MODEL),
        ),
    ]
