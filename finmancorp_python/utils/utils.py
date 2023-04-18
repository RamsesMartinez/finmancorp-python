import os
from datetime import datetime
from uuid import uuid4

from django.utils.text import slugify


def upload_to(instance, filename):
    app_label = instance._meta.app_label
    model_name = slugify(instance.__class__.__name__)
    today = datetime.now().strftime("%Y/%m/%d")
    extension = os.path.splitext(filename)[1]
    random_filename = str(uuid4()) + extension
    return f"{app_label}/{model_name}_image/{today}/{random_filename}"
