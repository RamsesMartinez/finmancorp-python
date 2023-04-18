from django_filters import rest_framework as dj_filters
from rest_framework.parsers import MultiPartParser

from finmancorp_python.images.api.serializers import ImageSerializer
from finmancorp_python.images.filters import ImageFilter
from finmancorp_python.images.models import Image
from finmancorp_python.utils.custom_mixins.mixins_serializers import CustomModelViewSet


class ImageViewSet(CustomModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = [MultiPartParser]
    filter_backends = [
        dj_filters.DjangoFilterBackend,
    ]
    filterset_class = ImageFilter
