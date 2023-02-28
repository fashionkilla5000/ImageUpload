from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers
from easy_thumbnails.files import get_thumbnailer

from rest_framework.request import Request
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username','password', 'email']


class SubscriptionPlanSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SubscriptionPlan
        fields = ['url','id','name','original_image','expiring_link','description']


class UserSubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    plan = serializers.SlugRelatedField(
        queryset=SubscriptionPlan.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = UserSubscription
        fields = ['url','id','user','plan']


class MyImageModelSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    thumbnail_400 = serializers.ImageField(read_only=True)
    thumbnail_200 = serializers.ImageField(read_only=True)
    thumbnail_width = serializers.IntegerField(read_only=True)
    thumbnail_height = serializers.IntegerField(read_only=True)
    avatar_thumbnail = serializers.ImageField(read_only=True)
    created_by = serializers.SlugRelatedField(many=False, slug_field='id', read_only=True)

    class Meta:
        model = MyImageModel
        fields = ('id', 'created_by', 'image', 'thumbnail_400', 'thumbnail_200','thumbnail_width','thumbnail_height','avatar_thumbnail')

    def to_representation(self, instance):
        user = self.context['request'].user
        basic_plan = UserSubscription.objects.filter(plan__name='basic', user=user)
        if basic_plan:
            ret = super().to_representation(instance)
            ret.pop('image', None)
            ret.pop('thumbnail_400', None)
            return ret
        else:
            ret = super().to_representation(instance)
            return ret







