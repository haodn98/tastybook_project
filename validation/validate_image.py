from django.core.exceptions import ValidationError
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

MAX_ALLOWED_LOGO_IMAGE_SIZE = 1 * 1024 * 1024


def validate_image_format(image: Image):
    valid_formats = ["PNG", "JPEG"]
    with Image.open(image) as img:
        format_ = img.format
        if format_ not in valid_formats:
            raise ValidationError(
                "Only PNG and JPEG are allowed."
            )
