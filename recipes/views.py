from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.serializers import RecipeSerializer, RecipeFilterSerializer
from recipes.manager import RecipesManager


class CreateRecipeView(ListCreateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        recipes = RecipesManager.get_all_recipes()
        return recipes


class UpdateRecipeView(RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        recipe = RecipesManager.get_recipe(self.kwargs["recipe_id"])
        return recipe

    def destroy(self, request, *args, **kwargs):
        RecipesManager.delete_recipe(kwargs.pop("recipe_id"))
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
