from rest_framework import serializers
from products.models import Product
from recipes.manager import RecipesManager
from recipes.utils import Utils


class RecipeSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    ingredients = serializers.DictField()
    complexity = serializers.IntegerField(min_value=1, max_value=5)
    process = serializers.ListField(child=serializers.CharField(), min_length=1)
    author = serializers.IntegerField(read_only=True)
    is_vegan = serializers.BooleanField(required=False, read_only=True)
    image = serializers.ImageField(required=False, read_only=True)

    def validate(self, attrs):
        ingredients = attrs["ingredients"]
        if not ingredients:
            raise serializers.ValidationError(f"No ingredients")
        products = [product.name for product in Product.objects.all()]
        for product in ingredients.keys():
            if product not in products:
                raise serializers.ValidationError(f'"{product}" product does not exist')

        return attrs

    def create(self, validated_data):
        recipe = RecipesManager.create_recipe(
            {
                "name": validated_data.pop("name"),
                "ingredients": validated_data.get("ingredients"),
                "complexity": validated_data.pop("complexity"),
                "process": validated_data.pop("process"),
                "author": self.context["request"].user.id,
                "is_vegan": Utils.check_if_vegan(validated_data.pop("ingredients"))
            }
        )
        return recipe

    def update(self, instance, validated_data):
        validated_data["is_vegan"] = Utils.check_if_vegan(validated_data.get("ingredients"))
        recipe = RecipesManager.update_recipe(instance["_id"], validated_data)
        return recipe


class RecipeFilterSerializer(serializers.Serializer):
    _id = serializers.CharField()
    name = serializers.CharField()
    ingredients = serializers.DictField(child=serializers.CharField())
    complexity = serializers.IntegerField()
    process = serializers.ListField(child=serializers.CharField())
    author = serializers.IntegerField()
    created_at = serializers.DateTimeField()
