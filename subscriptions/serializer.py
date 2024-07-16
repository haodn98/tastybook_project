from rest_framework import serializers

from subscriptions.models import Subscription
from recipes.manager import RecipesManager


class CreateSubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = ["user", "recipe_id"]

    def validate(self, attrs):
        user_id = attrs.get("user").id
        recipe_id = attrs.get("recipe_id")
        if RecipesManager.is_author(user_id, recipe_id):
            raise serializers.ValidationError("Can`t subscribe to your own recipe")
        if Subscription.objects.filter(user=user_id, recipe_id=recipe_id).exists():
            raise serializers.ValidationError("Subscription already exists")
        return attrs
