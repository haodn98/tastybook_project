from django.urls import path
from recipes import views


app_name = 'recipe'

urlpatterns = [
    path(
        'create/',
        views.CreateRecipeView.as_view(),
        name="recipe_create_view",
    ),
    path(
       'details/<str:recipe_id>/',
       views.UpdateRecipeView.as_view(),
       name="recipe_details_view"
    ),
    path(
        'recipe_filter/by_products/',
        views.RecipeFilterByProduct.as_view(),
        name="recipe_product_filter_view"
    ),
    path(
        'recipe_filter/by_author/',
        views.RecipeFilterByAuthor.as_view(),
        name="recipe_author_filter_view"
    ),
]
