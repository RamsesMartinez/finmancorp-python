from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractBaseModel(models.Model):
    """Django custom base model.
    BaseModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + is_active (Boolean): Indicates if the object is active.
        + created_at (DateTime): Store the datetime the object was created.
        + modified_at (DateTime): Store the last datetime the object was modified.
    """

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Indicates if the record should be treated as active. Uncheck this option instead of deleting the record."
        ),
    )
    created_at = models.DateTimeField(
        verbose_name="Creation date",
        auto_now_add=True,
        help_text="Last date the record was modified.",
    )
    modified_at = models.DateTimeField(
        verbose_name="Última modificación",
        auto_now=True,
        help_text="Última fecha en que el registro fue modificado",
    )
    created_by = models.ForeignKey(
        verbose_name="Creating user",
        to="users.User",
        on_delete=models.CASCADE,
        default=1,
        related_name="%(app_label)s_%(class)s_created",
    )
    modified_by = models.ForeignKey(
        verbose_name="Editing user",
        to="users.User",
        on_delete=models.CASCADE,
        null=True,
        related_name="%(app_label)s_%(class)s_modified",
    )

    class Meta:
        """Meta option."""

        abstract = True

        ordering = ["-created_at", "-modified_at"]

    def __str__(self):
        return self.id
