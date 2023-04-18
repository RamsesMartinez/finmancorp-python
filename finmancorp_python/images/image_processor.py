from io import BytesIO

from PIL import Image as PILImage


class ImageProcessor:
    def __init__(self, image_file):
        self.image_file = image_file
        self.image = PILImage.open(image_file)

    def scale(self, width, height):
        self.image = self.image.resize((width, height), PILImage.ANTIALIAS)

    def crop(self, width, height):
        self.image.thumbnail((width, height), PILImage.ANTIALIAS)
        self.image = self.image.crop((0, 0, width, height))

    def save(self):
        buffer = BytesIO()
        image_format = self.image_file.image.format or "JPEG"
        self.image.save(buffer, format=image_format)
        buffer.seek(0)
        return buffer
