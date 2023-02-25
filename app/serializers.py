from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import MyImageModel


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class MyImageModelSerializer(serializers.ModelSerializer):
    thumbnail_400 = serializers.ImageField(read_only=True)
    thumbnail_200 = serializers.ImageField(read_only=True)

    class Meta:
        model = MyImageModel
        fields = ('id', 'image', 'thumbnail_400', 'thumbnail_200')


