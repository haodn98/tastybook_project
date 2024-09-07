from django.urls import path
from images.views import ImageCreateAPIView

app_name = "images"

urlpatterns = [
    path(
        "recipe/add/",
        ImageCreateAPIView.as_view(),
        name="recipe_image_create",
    ),
    path(
        "recipe/delete/<int:image_pk>",
        ImageCreateAPIView.as_view(),
        name="recipe_image_delete",
    )
]
