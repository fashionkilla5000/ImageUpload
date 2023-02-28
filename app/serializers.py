from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username','password', 'email']


class ThumbnailSizeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ThumbnailSize
        fields = ['url','id','size']


class SubscriptionPlanSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    thumbnail_size = serializers.SlugRelatedField(
        queryset=ThumbnailSize.objects.all(),
        many=True,
        slug_field='size'
    )

    class Meta:
        model = SubscriptionPlan
        fields = ['url','id','name','thumbnail_size','original_image','expiring_link','description']


class UserSubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        many=True,
        slug_field='username'
    )
    plan = serializers.SlugRelatedField(
        queryset=SubscriptionPlan.objects.all(),
        many=True,
        slug_field='name'
    )

    class Meta:
        model = UserSubscription
        fields = ['url','id','user','plan']


class MyImageModelSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.ImageField()
    thumbnail_400 = serializers.ImageField(read_only=True)
    thumbnail_200 = serializers.ImageField(read_only=True)
    created_by = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail'
    )

    class Meta:
        model = MyImageModel
        fields = ('id', 'created_by', 'image', 'thumbnail_400', 'thumbnail_200')

    def to_representation(self, instance):
        user = self.context['request'].user

        basic_plan = UserSubscription.objects.filter(user=user)

        if basic_plan:
            ret = super().to_representation(instance)
            ret.pop('image', None)
            ret.pop('thumbnail_400', None)
            return ret
        else:
            ret = super().to_representation(instance)
            return ret




