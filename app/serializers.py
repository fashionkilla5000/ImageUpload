from django.core.signing import TimestampSigner

from .models import *
from rest_framework import serializers


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
        fields = ['url', 'id', 'user', 'plan']


class MyImageModelSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    thumbnail_400 = serializers.ImageField(read_only=True)
    thumbnail_200 = serializers.ImageField(read_only=True)
    avatar_thumbnail = serializers.ImageField(read_only=True)
    created_by = serializers.SlugRelatedField(many=False, slug_field='id', read_only=True)
    expiration_date = serializers.DateTimeField(read_only=True)
    expiration_time = serializers.IntegerField()
    expiration_link = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = MyImageModel
        fields = ('id', 'created_by', 'image', 'thumbnail_400', 'thumbnail_200', 'avatar_thumbnail',
                  'expiration_time', 'created_at','expiration_date','expiration_link')

    def get_expiration_link(self, obj):
        signer = TimestampSigner()
        try:
            return signer.unsign(obj.expiration_link, max_age=obj.expiration_time)
        except:
            obj.expiration_link = 'expired'
            return obj.expiration_link

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








