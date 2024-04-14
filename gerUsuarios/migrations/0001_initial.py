# Generated by Django 4.2.11 on 2024-04-14 18:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nome', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('data_nascimento', models.DateField(null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Contato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ativo', models.BooleanField(default=True)),
                ('email', models.EmailField(max_length=60)),
                ('tel', models.CharField(max_length=11)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ativo', models.BooleanField(default=True)),
                ('logradouro', models.CharField(max_length=60)),
                ('bairro', models.CharField(max_length=30)),
                ('cep', models.CharField(max_length=8)),
                ('complemento', models.CharField(max_length=30, null=True)),
                ('num_casa', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Setor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ativo', models.BooleanField(default=True)),
                ('nome', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ativo', models.BooleanField(default=True)),
                ('nome', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tipo_Matricula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ativo', models.BooleanField(default=True)),
                ('descricao', models.CharField(max_length=60)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Setor_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ativo', models.BooleanField(default=True)),
                ('setor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='setor_user_setor', to='gerUsuarios.setor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='setor_user_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ativo', models.BooleanField(default=True)),
                ('matricula', models.CharField(max_length=19, unique=True)),
                ('validade', models.DateField(null=True)),
                ('expedicao', models.DateField()),
                ('tipo_matricula', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='tipo_matricula', to='gerUsuarios.tipo_matricula')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='matricula_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ativo', models.BooleanField(default=True)),
                ('nome', models.CharField(max_length=30)),
                ('cnpj', models.CharField(max_length=14, unique=True)),
                ('contato', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='empresa_contato', to='gerUsuarios.contato')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='contato',
            name='endereco',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='contato_endereco', to='gerUsuarios.endereco'),
        ),
        migrations.AddField(
            model_name='user',
            name='contato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='user_contato', to='gerUsuarios.contato'),
        ),
        migrations.AddField(
            model_name='user',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='user_empresa', to='gerUsuarios.empresa'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='setores',
            field=models.ManyToManyField(through='gerUsuarios.Setor_User', to='gerUsuarios.setor'),
        ),
        migrations.AddField(
            model_name='user',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='user_tipo', to='gerUsuarios.tipo'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
