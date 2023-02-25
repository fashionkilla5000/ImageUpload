from django.contrib.auth.models import User, Group
from .models import MyImageModel, UserSubscription, SubscriptionPlan
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class MyImageModelSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    thumbnail_400 = serializers.ImageField(read_only=True)
    thumbnail_200 = serializers.ImageField(read_only=True)
    created_by = serializers.SlugRelatedField(many=False, slug_field='id', read_only=True)

    class Meta:
        model = MyImageModel
        fields = ('id', 'created_by', 'image', 'thumbnail_400', 'thumbnail_200')

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




