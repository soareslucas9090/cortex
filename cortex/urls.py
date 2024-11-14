"""
URL configuration for cortex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Importação feita para utilizar classe customizada que permite apenas superusuários
# terem acesso ao Painel Admin
from gerUsuarios.admin import admin_custom_site

from .view_jwt import TokenObtainPairViewDOC, TokenRefreshViewDOC, TokenVerifyViewDOC

urlpatterns = [
    path("cortex/admin/", admin_custom_site.urls),
    path(
        "cortex/api/token/", TokenObtainPairViewDOC.as_view(), name="token_obtain_pair"
    ),
    path(
        "cortex/api/token/refresh/", TokenRefreshViewDOC.as_view(), name="token_refresh"
    ),
    path("cortex/api/token/verify/", TokenVerifyViewDOC.as_view(), name="token_verify"),
    path("cortex/api/gerusuarios/v1/", include("gerUsuarios.urls")),
    path("cortex/api/soticon/v1/", include("soticon.urls")),
    path("cortex/api/watt/v1/", include("watt.urls")),
    path("cortex/api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "cortex/api/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(
        "cortex/api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("__debug__/", include("debug_toolbar.urls")),
]
