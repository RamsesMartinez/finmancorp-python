from django.db import models

from finmancorp_python.utils.models import AbstractBaseModel
from finmancorp_python.utils.utils import upload_to
from django.utils.translation import gettext_lazy as _


class Image(AbstractBaseModel):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255,
        unique=True,
        db_index=True
    )
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to=upload_to
    )
    width = models.PositiveSmallIntegerField(
        verbose_name=_("Width"),
    )
    height = models.PositiveSmallIntegerField(
        verbose_name=_("Height"),
    )

    def __str__(self):
        return self.title
