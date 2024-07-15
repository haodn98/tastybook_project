from products.models import Product


def check_if_vegan(ingredients):
    filtered_ingredients = Product.objects.filter(name__in=ingredients)
    return all(ingredient.is_vegan for ingredient in filtered_ingredients)
