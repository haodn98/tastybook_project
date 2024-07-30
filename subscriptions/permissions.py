from rest_framework.permissions import BasePermission, SAFE_METHODS

from recipes.manager import RecipesManager


class IsUsersSubscription(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
