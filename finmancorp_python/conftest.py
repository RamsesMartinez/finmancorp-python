import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from finmancorp_python.users.models import User
from finmancorp_python.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user_factory(db) -> User:
    return UserFactory()


@pytest.fixture
def api_public_client() -> APIClient:
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def create_token(db, user_factory):
    def make_token(user: User = None):
        if user is None:
            user = user_factory
        token = RefreshToken.for_user(user)
        token["id"] = user.id
        token["username"] = user.username
        return str(token.access_token)

    return make_token


@pytest.fixture
def api_client_with_admin_credentials(api_public_client, create_token):
    def make_api_client(user: User = None) -> APIClient:
        token = create_token(
            user=user,
        )
        api_public_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        return api_public_client

    return make_api_client
