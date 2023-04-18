import os
from io import BytesIO

from django.core.files import File
from django.core.files.base import ContentFile
from rest_framework import serializers
from PIL import Image as PILImage

from finmancorp_python.images.image_processor import ImageProcessor
from finmancorp_python.images.models import Image


class ImageSerializer(serializers.ModelSerializer):
    resize_mode = serializers.ChoiceField(
        choices=[('scale', 'scale'), ('crop', 'crop')], required=False, write_only=True
    )

    class Meta:
        model = Image
        fields = ['id', 'title', 'image', 'width', 'height', 'resize_mode']
        extra_kwargs = {
            'width': {'required': False},
            'height': {'required': False}
        }

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)

        # Use default dimensions if not provided
        image = PILImage.open(validated_data['image'].file)
        validated_data['width'] = validated_data.get('width', image.width)
        validated_data['height'] = validated_data.get('height', image.height)

        return validated_data

    # noinspection PyMethodMayBeStatic
    def create(self, validated_data):
        # Get the resize mode and image data
        resize_mode = validated_data.pop('resize_mode', 'scale')
        image_file = validated_data.pop('image')
        img_name = image_file.name

        # Scale or crop the image
        image_processor = ImageProcessor(image_file)
        if resize_mode == 'scale':
            image_processor.scale(validated_data['width'], validated_data['height'])
        elif resize_mode == 'crop':
            image_processor.crop(validated_data['width'], validated_data['height'])

        # Save the modified image to a buffer
        buffer = image_processor.save()
        image_content = ContentFile(buffer.getvalue())
        validated_data['image'] = image_content
        # Call the parent create() method to save the model instance
        image_obj = super().create(validated_data)
        # Save the modified image file to the storage
        image_obj.image.save(img_name, File(buffer), save=False)
        return image_obj
