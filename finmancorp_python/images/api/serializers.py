import os
from io import BytesIO

from django.core.files import File
from django.core.files.base import ContentFile
from rest_framework import serializers
from PIL import Image as PILImage

from finmancorp_python.images.models import Image


class ImageSerializer(serializers.ModelSerializer):
    resize_mode = serializers.ChoiceField(
        choices=[('scale', 'scale'), ('crop', 'crop')], required=False, default='scale'
    )

    class Meta:
        model = Image
        fields = ['id', 'title', 'image', 'width', 'height', 'resize_mode']
        extra_kwargs = {
            'width': {'required': False},
            'height': {'required': False}
        }

    # noinspection PyMethodMayBeStatic
    def create(self, validated_data):
        resize_mode = validated_data.pop('resize_mode', 'scale')
        image = PILImage.open(validated_data['image'].file)
        image_format = image.format
        img_name = validated_data['image'].name
        width = validated_data.get('width', image.width)
        height = validated_data.get('height', image.height)

        # Update validated_data with the dimensions
        validated_data['width'] = width
        validated_data['height'] = height

        # Scale or crop the image
        if resize_mode == 'scale':
            image = image.resize((width, height), PILImage.ANTIALIAS)
        elif resize_mode == 'crop':
            image.thumbnail((width, height), PILImage.ANTIALIAS)
            image = image.crop((0, 0, width, height))

        buffer = BytesIO()
        image.save(buffer, image_format)
        image_content = ContentFile(buffer.getvalue())
        validated_data['image'] = image_content
        image_obj = super().create(validated_data)
        image_obj.image.save(img_name, File(buffer), save=False)
        return image_obj
