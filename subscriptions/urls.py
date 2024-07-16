from django.urls import path
from subscriptions import views

app_name = 'Subscription'

urlpatterns = [
    path(
        'create/',
        views.SubscriptionCreate.as_view(),
        name="subscription_create"
    )
]
