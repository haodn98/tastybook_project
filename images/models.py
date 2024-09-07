from django.core.validators import FileExtensionValidator
from django.db import models

from authentication.models import CustomUser


def image_directory_path(instance,filename):
    return f"recipe_images/{filename}"


class RecipeImage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="created_images"
    )
    image_path = models.ImageField(
        upload_to=image_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=["jpeg", "png", "jpg"])],
        blank=True
    )
    image_size = models.PositiveIntegerField(null=True)
    hash_md5 = models.CharField(max_length=32, blank=True)
    is_approved = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    recipe_id = models.CharField(max_length=24, default="")
