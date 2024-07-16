from datetime import datetime

from django.db import models


class Subscription(models.Model):
    user = models.ForeignKey("authentication.CustomUser", on_delete=models.CASCADE)
    recipe_id = models.CharField(max_length=24)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_subscription(cls, *args, **kwargs):
        return cls.objects.get(**kwargs)

    @classmethod
    def get_subscriptions(cls, *args, **kwargs):
        return cls.objects.filter(**kwargs)

    def get_info(self):
        data = {
            "subscribed_at": self.subscribed_at,
            "user": self.user,
            "recipe_id": self.recipe_id
        }
        return data
