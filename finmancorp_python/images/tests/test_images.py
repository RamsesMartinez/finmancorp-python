import io
import random

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from faker import Faker
from PIL import Image as PILImage
from rest_framework import status

from finmancorp_python.images.models import Image

fake = Faker()


@pytest.fixture
def create_image(db):
    return Image.objects.create(
        title=fake.text(12),
        image=f"{fake.text(12)}.png",
        width=random.randint(50, 100),
        height=random.randint(50, 100),
    )


class TestImage:
    def create_request_image(self):
        # Create a test image with 100x100 size
        image = PILImage.new("RGBA", size=(100, 100), color=(255, 0, 0, 0))
        with io.BytesIO() as output:
            image.save(output, format="PNG")
            output.seek(0)
            image_data = output.read()
            image_file = SimpleUploadedFile("test.png", image_data, content_type="image/png")
            image_file.content_disposition = 'attachment; filename="test.png"'
            return image_file

    def test_create_valid_image(self, api_client_with_admin_credentials):
        url = reverse("api:images-list")
        api_client = api_client_with_admin_credentials()

        image_data = {
            "title": "Test image",
            "width": 50,
            "height": 50,
            "image": self.create_request_image(),
        }
        response = api_client.post(url, data=image_data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_invalid_image(self, api_client_with_admin_credentials):
        url = reverse("api:images-list")
        api_client = api_client_with_admin_credentials()

        image_data = {
            "title": "Invalid image",
            "image": SimpleUploadedFile("test.png", b"invalid image data", content_type="image/png"),
        }
        response = api_client.post(url, data=image_data, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_images(self, api_client_with_admin_credentials, create_image):
        url = reverse("api:images-list")
        api_client = api_client_with_admin_credentials()
        response = api_client.get(
            url,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] > 0

    def test_get_image_detail(self, api_client_with_admin_credentials, create_image):
        image = create_image
        url = reverse("api:images-detail", kwargs={"pk": image.id})
        api_client = api_client_with_admin_credentials()
        response = api_client.get(
            url,
        )
        assert response.status_code == status.HTTP_200_OK
