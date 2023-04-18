from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .serializers import UserLoginTokenPairSerializer

User = get_user_model()


class UserAuthViewSet(viewsets.GenericViewSet):
    """Vista de API para autenticación de usuario."""

    serializer_class = TokenRefreshSerializer

    def get_permissions(self):
        """Asigna permisos según la acción"""
        permissions = [AllowAny]

        return (permission() for permission in permissions)

    @action(detail=False, methods=["post"], url_path="token/refresh")
    def token_refresh(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            data = {"detail": e.args[0], "code": "token_expired"}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.validated_data, status.HTTP_200_OK)


@method_decorator(transaction.non_atomic_requests, name="dispatch")
class UserAuthNonAtomicViewSet(viewsets.GenericViewSet):
    serializer_class = UserLoginTokenPairSerializer

    def get_permissions(self):
        """Asigna permisos según la acción"""
        permissions = [AllowAny]

        return (permission() for permission in permissions)

    @action(detail=False, methods=["post"], url_path="token")
    def token(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
