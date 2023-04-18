from django.contrib import admin

from finmancorp_python.images.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image", "created_by", "modified_by")
    list_display_links = (
        "id",
        "title",
    )
