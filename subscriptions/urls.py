from django.urls import path
from subscriptions import views

app_name = 'Subscription'

urlpatterns = [
    path(
        '',
        views.SubscriptionCreate.as_view(),
        name="subscription_create"
    ),
    path(
        'details/<str:sub_id>/',
        views.SubscriptionDetailsDelete.as_view(),
        name="subscription_create"
    )
]
