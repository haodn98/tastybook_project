from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path(
        '',
        views.ProductListCreateView.as_view(),
        name="product_create_view",
    ),
    path(
       '<int:product_id>/',
       views.ProductDetailsUpdateDelete.as_view(),
       name="product_details_view"
    ),
]
