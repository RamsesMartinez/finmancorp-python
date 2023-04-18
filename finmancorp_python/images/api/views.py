from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from PIL import Image as PILImage
from rest_framework.response import Response

from finmancorp_python.images.api.serializers import ImageSerializer
from finmancorp_python.images.models import Image


class ImageViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser]

    def create(self, request):
        serializer = ImageSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            # Save image object in the database
            serializer.save()

            # Resize image
            img = PILImage.open(serializer.instance.image.path)
            img = img.resize((serializer.instance.width, serializer.instance.height))
            img.save(serializer.instance.image.path)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        image = get_object_or_404(Image, pk=pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)
