from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from images.models import RecipeImage
from recipes.permissions import IsRecipeAuthor
from recipes.serializers import RecipeSerializer, RecipeFilterSerializer
from recipes.manager import RecipesManager
from recipes.notifications import update_recipe_notification, delete_recipe_notification
from subscriptions.models import Subscription


class CreateRecipeView(ListCreateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        recipes = RecipesManager.get_all_recipes()
        return recipes


class UpdateRecipeView(RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer
    # permission_classes = (IsAuthenticated, IsRecipeAuthor | IsAdminUser)

    def get_object(self):
        recipe = RecipesManager.get_recipe(self.kwargs["recipe_id"])
        recipe_dict = dict(recipe)
        recipe_image = RecipeImage.objects.filter(recipe_id=self.kwargs["recipe_id"]).first()
        recipe_dict["image"] = str(recipe_image.image_path)
        self.check_object_permissions(request=self.request, obj=recipe_dict)
        print(recipe_dict)
        return recipe_dict

    @update_recipe_notification
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @delete_recipe_notification
    def destroy(self, request, *args, **kwargs):
        recipe_id = kwargs.get("recipe_id")
        RecipesManager.delete_recipe(recipe_id)
        subs = Subscription.objects.filter(recipe_id=recipe_id)
        if subs.exists():
            subs.delete()
        return Response({"message": "Recipe was deleted"}, status=status.HTTP_204_NO_CONTENT)


class RecipeFilterByProduct(ListAPIView):
    serializer_class = RecipeFilterSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        products_in_recipe = self.request.GET.get("ingredients", '').split(',')
        if products_in_recipe:
            recipes = RecipesManager.recipe_filter(
                {
                    "$and": [
                        {f"ingredients.{product}": {"$exists": True}}
                        for product in products_in_recipe
                    ]
                }
            )
            return recipes
        return []


class RecipeFilterByAuthor(ListAPIView):
    serializer_class = RecipeFilterSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        author = self.request.GET.get("author", '')
        if author:
            recipes = RecipesManager.recipe_filter(
                {
                    "author": int(author)
                }
            )
            return recipes
        return []
