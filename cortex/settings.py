import os
from pathlib import Path

from dotenv import load_dotenv

from .rest_framework_settings import *
from .spectacular_settings import *

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
SECRET_KEY = os.environ.get("secretKeyDjango")

DEBUG = os.environ.get("debugMode")
ALLOWED_HOSTS = [os.environ.get("allowedHosts")]
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

CSRF_TRUSTED_ORIGINS = os.getenv("csrfTrustedOrigins", "").split(",")

CORS_ALLOW_ALL_ORIGINS: True

INTERNAL_IPS = os.getenv("internalIPs", "").split(",")

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
    "ouvidoria",
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


STATIC_URL = "/static/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
