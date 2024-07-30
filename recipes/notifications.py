from recipes.manager import RecipesManager
from subscriptions.models import Subscription

from .tasks import send_email_task

def update_recipe_notification(func):
    def inner(*args, **kwargs):
        response = func(*args, **kwargs)
        recipe_id = kwargs["recipe_id"]
        recipe = RecipesManager.get_recipe(kwargs["recipe_id"])
        users = Subscription.objects.filter(recipe_id=recipe_id)
        if users.exists():
            for user in users:
                email_body = f"Hello {user.user.username} Recipe {recipe['name']} has been updated \n"
                send_email_task.delay(user.user, email_body)
        return response
    return inner


def delete_recipe_notification(func):
    def inner(*args, **kwargs):
        recipe_id = kwargs["recipe_id"]
        recipe = RecipesManager.get_recipe(recipe_id)
        users = Subscription.objects.filter(recipe_id=recipe_id)
        if users.exists():
            for user in users:
                email_body = f"Hello {user.user.username} Recipe {recipe['name']} was deleted "
                send_email_task.delat(user.user, email_body)
        response = func(*args, **kwargs)
        return response
    return inner
