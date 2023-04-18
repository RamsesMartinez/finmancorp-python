from django.contrib.auth import get_user_model, user_logged_in
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserLoginTokenPairSerializer(TokenObtainSerializer):
    # noinspection PyMethodMayBeStatic
    def get_view_token(self, user, request):
        token = RefreshToken.for_user(user)
        token["id"] = user.id
        token["email"] = user.email
        return token

    # noinspection PyMethodMayBeStatic
    def authenticate_user(self, request, email=None, password=None):
        if email is None or password is None:
            raise exceptions.AuthenticationFailed(_("Please check your credentials"))

        user = User.objects.filter(email=email)
        if not user.exists():
            raise exceptions.AuthenticationFailed(_("User does not exist"))

        user = user.first()
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed(_("Please check your login credentials."))

        return user

    def validate(self, attr):
        authenticate_kwargs = {
            self.username_field: attr[self.username_field],
            "password": attr["password"],
        }
        user_id = attr.get("user_id", None)
        if user_id:
            authenticate_kwargs.update({"user_id": attr["user_id"]})

        request = self.context["request"]

        user = self.authenticate_user(request=request, **authenticate_kwargs)

        refresh = self.get_view_token(user, request)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }
