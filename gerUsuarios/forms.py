from django import forms
from django.contrib.auth.models import Permission

from .models import *


class AdminPortalUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["cpf", "email", "password", "nome", "is_active", "is_admin"]

    def save(self, commit=True):
        user = super().save(commit=False)

        # Verifica se a senha já foi criptografada, se não, siginifica que o usuário está trocando a senha
        if not self.cleaned_data["password"].startswith(
            ("pbkdf2_sha256$", "bcrypt$", "argon2$", "django.contrib.auth.hashers")
        ):
            user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

            if user.is_superuser:
                user.is_admin = True
                user.is_staff = True
                permissions = Permission.objects.all()
                user.user_permissions.set(permissions)
            else:
                user.is_staff = False
                none_permissions = Permission.objects.none()
                user.user_permissions.set(none_permissions)

            user.save()

        return user
