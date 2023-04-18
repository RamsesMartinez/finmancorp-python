from typing import Any

from django.core.exceptions import FieldError
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response


class CustomCreateModelMixin(mixins.CreateModelMixin):
    """Class to overwrite the creation of an object by injecting the user in the request"""

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request.data["created_by"] = request.user.id
        return super().create(request, *args, **kwargs)


class CustomUpdateModelMixin(mixins.UpdateModelMixin):
    """Class to overwrite the update of an object by injecting the user in the request."""

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request.data["modified_by"] = request.user.id
        return super().update(request, *args, **kwargs)


class CustomDestroyModelMixin(mixins.DestroyModelMixin):
    """Class to overwrite the deletion of an object by changing the is_active=False attribute."""

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class CustomListModelMixin:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except FieldError as e:
            raise ValidationError({"error": str(e)})


class CustomModelViewSet(
    CustomCreateModelMixin,
    CustomUpdateModelMixin,
    mixins.RetrieveModelMixin,
    CustomDestroyModelMixin,
    CustomListModelMixin,
    viewsets.GenericViewSet,
):
    """Un ViewSet customizado para proveer el método create()"""

    pass
