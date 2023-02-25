from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from app.serializers import UserSerializer, GroupSerializer

from rest_framework.parsers import MultiPartParser, FormParser

from .models import MyImageModel
from .serializers import MyImageModelSerializer
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyImageModelViewSet(viewsets.ModelViewSet):
    serializer_class = MyImageModelSerializer
    parser_classes = (MultiPartParser, FormParser)

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


