from datetime import timedelta

from django.utils import timezone
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
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
        user = self.request.user

        user_plan = UserSubscription.objects.get(user=user).plan
        get_size = SubscriptionPlan.objects.get(name=user_plan)

        serializer.validated_data['created_by'] = user
        serializer.validated_data['thumbnail_width'] = get_size.custom_thumbnail_width
        serializer.validated_data['thumbnail_height'] = get_size.custom_thumbnail_height
        serializer.validated_data['expiration_date'] = timezone.now() + \
                                                       timedelta(seconds=serializer.save().expiration_time)
        serializer.validated_data['expiration_link'] = self.request.build_absolute_uri(serializer.save().image.url)
        serializer.save()

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = MyImageModel.objects.all()
        else:
            queryset = MyImageModel.objects.filter(created_by=user)
        return queryset




