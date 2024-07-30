from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from subscriptions.models import Subscription
from subscriptions.permissions import IsUsersSubscription
from subscriptions.serializer import SubscriptionSerializer


class SubscriptionCreate(ListCreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Subscription.objects.all()


class SubscriptionDetailsDelete(RetrieveDestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated, IsAdminUser, IsUsersSubscription)
    queryset = Subscription.objects.all()
    lookup_url_kwarg = "sub_id"
