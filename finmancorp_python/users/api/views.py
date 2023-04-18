from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .serializers import UserSerializer, UserLoginTokenPairSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


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
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
