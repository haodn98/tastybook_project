from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from subscriptions.models import Subscription
from subscriptions.serializer import CreateSubscriptionSerializer


class SubscriptionCreate(ListCreateAPIView):
    serializer_class = CreateSubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Subscription.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
