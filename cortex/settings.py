"""
Django settings for cortex project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

from .rest_framework_settings import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


SECRET_KEY = os.environ.get("secretKeyDjango")

if SECRET_KEY:
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
else:
    from .env import *

    SECRET_KEY = secretKeyDjango
    DEBUG = debug
    ALLOWED_HOSTS = allowedHosts
    DATABASES = {
        "default": {
            "ENGINE": bdEngine,
            "NAME": bdName,
            "USER": bdUser,
            "PASSWORD": bdPass,
            "HOST": bdHost,
            "PORT": bdPort,
        }
    }


CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.18.69:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://cortexfront.web.app",
    "https://web-5gnex1an3lly.up-us-nyc1-k8s-1.apps.run-on-seenode.com",
    "https://cloud.seenode.com",
]

CORS_ALLOW_ALL_ORIGINS: True
"""
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.18.69:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://cortexfront.web.app",
    "https://web-5gnex1an3lly.up-us-nyc1-k8s-1.apps.run-on-seenode.com",
    "https://cloud.seenode.com",
]
"""
CORS_ALLOW_METHODS = ["*"]

AUTH_USER_MODEL = "gerUsuarios.User"
ACCOUNT_AUTHENTICATION_METHOD = "cpf"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_USERNAME_REQUIRED = False


# Application definition

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
]

ROOT_URLCONF = "cortex.urls"

INTERNAL_IPS = ["127.0.0.1", "https://soareslukas9090.pythonanywhere.com/"]


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


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
