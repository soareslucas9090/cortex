import os
from pathlib import Path

from dotenv import load_dotenv

from .rest_framework_settings import *
from .spectacular_settings import *

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
# SECRET_KEY do Django, usada para criptografia
SECRET_KEY = os.environ.get("secretKeyDjango")
# Configura se o Django está em modo de DEBUG ou não
DEBUG = os.environ.get("debugMode")
# Indica todos os hosts autorizados a fazer requisições para o APP
ALLOWED_HOSTS = [os.environ.get("allowedHosts")]
# Configura o banco de dados
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("bdEngine"),
        "NAME": os.environ.get("bdName"),
        "USER": os.environ.get("bdUser"),
        "PASSWORD": os.environ.get("bdPass"),
        "HOST": os.environ.get("bdHost"),
        "PORT": os.environ.get("bdPort"),
    }
}
# Armazena os endereços confiáveis para CSRF
CSRF_TRUSTED_ORIGINS = os.environ.get(
    "csrfTrustedOriginsANDcorsOriginWhitelist", ""
).split(",")
# Indica quais são os endereços internos
INTERNAL_IPS = os.environ.get("internalIPs", "").split(",")
# Armazena os endereços confiáveis para CORS
CORS_ORIGIN_WHITELIST = os.environ.get(
    "csrfTrustedOriginsANDcorsOriginWhitelist", ""
).split(",")

# Email padrão para o envio de emails do Django
DEFAULT_FROM_EMAIL = os.environ.get("DefaultEmailForPasswordReset")
EMAIL_HOST_USER = os.environ.get("DefaultEmailForPasswordReset")
# Senha do Email. O Google exige que seja criado uma Senha de APP
EMAIL_HOST_PASSWORD = os.environ.get("EmailPassword")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# As configurações padrões são para o serviço de email do Google, mas podem ser alteradas
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

CORS_ALLOW_ALL_ORIGINS: True

CORS_ALLOW_METHODS = ["*"]

AUTH_USER_MODEL = "gerUsuarios.User"
ACCOUNT_AUTHENTICATION_METHOD = "cpf"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_USERNAME_REQUIRED = False


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "debug_toolbar",
    "rest_framework_simplejwt",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "gerUsuarios",
    "soticon",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]

ROOT_URLCONF = "cortex.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cortex.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
