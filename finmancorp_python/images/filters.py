import django_filters

from finmancorp_python.images.models import Image


class ImageFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Image
        fields = ["title"]
