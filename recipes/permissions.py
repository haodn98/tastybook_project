from rest_framework.permissions import BasePermission, SAFE_METHODS

from recipes.manager import RecipesManager


class IsRecipeAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        recipe = obj["_id"]
        return RecipesManager.is_author(user.id, recipe)
