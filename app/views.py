from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions

from rest_framework.parsers import MultiPartParser, FormParser

from .models import *
from .serializers import *
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ThumbnailSizeViewSet(viewsets.ModelViewSet):
    queryset = ThumbnailSize.objects.all()
    serializer_class = ThumbnailSizeSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyImageModelViewSet(viewsets.ModelViewSet):
    serializer_class = MyImageModelSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['created_by'] = self.request.user
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = MyImageModel.objects.all()
        else:
            queryset = MyImageModel.objects.filter(created_by=user)
        return queryset


