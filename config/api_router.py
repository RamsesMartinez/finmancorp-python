from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from finmancorp_python.images.api.views import ImageViewSet
from finmancorp_python.users.api.views import UserAuthNonAtomicViewSet, UserAuthViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("auth", UserAuthViewSet, basename="auth")
router.register("auth", UserAuthNonAtomicViewSet, basename="auth_not_atomic")
router.register("images", ImageViewSet, basename="images")


app_name = "api"
urlpatterns = router.urls
