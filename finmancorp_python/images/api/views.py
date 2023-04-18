from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from finmancorp_python.images.api.serializers import ImageSerializer
from finmancorp_python.images.models import Image
from finmancorp_python.utils.custom_mixins.mixins_serializers import CustomModelViewSet


class ImageViewSet(CustomModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = [MultiPartParser]
