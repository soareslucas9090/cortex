import os
from datetime import timedelta

from .env import *

REST_FRAMEWORK = {
    # Autenticação por seção está comentada pois foi implementada a por token, mas pode ter as duas
    "DEFAULT_AUTHENTICATION_CLASSES": (
        #'rest_framework.authentication.SessionAuthentication',
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # Somente é autorizado o acesso, seja get, seja update/delete/post se autenticado
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    # Paginação
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DATE_INPUT_FORMATS": ["%d-%m-%y", "%d-%m-%Y", "%d/%m/%y", "%d/%m/%Y"],
    "TIME_INPUT_FORMATS": [
        "%d-%m-%yT%H:%M:%S",
        "%d-%m-%YT%H:%M:%S",
        "%d/%m/%yT%H:%M:%S",
        "%d/%m/%YT%H:%M:%S",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "BLACKLIST_AFTER_ROTATION": False,
    "SIGNING_KEY": os.environ.get("secretKeyJWT"),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}
