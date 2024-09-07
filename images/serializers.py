from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from images.models import RecipeImage
from validation.validate_image import validate_image_format
from recipes.manager import RecipesManager


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeImage
        fields = (
            "image_path",
            "created_by",
            "image_size",
            "hash_md5",
            "is_approved",
            "is_deleted",
            "created_at",
            "recipe_id",
        )

        read_only_fields = (
            "created_by",
            "image_size",
            "hash_md5",
            "is_approved",
            "is_deleted",
            "created_at",
        )

    def validate(self, attrs):
        validate_image_format(attrs.get("image_path"))
        recipe_id = RecipesManager.get_recipe(attrs.get("recipe_id"))
        if not recipe_id:
            raise ValidationError(f"Recipe with ID {recipe_id} does not exist.")
        return attrs
