from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Nenhuma lógica sobreescrita, apenas para fins de documentação


@extend_schema(tags=["Auth"])
class TokenObtainPairViewDOC(TokenObtainPairView):
    pass


@extend_schema(tags=["Auth"])
class TokenRefreshViewDOC(TokenRefreshView):
    pass


@extend_schema(tags=["Auth"])
class TokenVerifyViewDOC(TokenVerifyView):
    pass
