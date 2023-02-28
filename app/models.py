from imagekit.processors import ResizeToFit
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import FileExtensionValidator

from django.db import models
from imagekit import ImageSpec, register
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.utils import get_field_info


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255, unique=True)
    original_image = models.BooleanField(blank=True, default=False)
    expiring_link = models.BooleanField(blank=True, default=False)
    description = models.TextField(blank=True)
    custom_thumbnail_width = models.PositiveIntegerField(blank=True,default=200)
    custom_thumbnail_height = models.PositiveIntegerField(blank=True,default=200)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan: SubscriptionPlan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)

    def __str__(self):
        return "User: " + str(self.user) + ", Plan: " + str(self.plan)


class AvatarThumbnail(ImageSpec):
    format = 'JPEG'
    options = {'quality': 60}

    @property
    def processors(self):
        model, field_name = get_field_info(self.source)
        return [ResizeToFill(model.thumbnail_width, model.thumbnail_height)]


register.generator('app:MyImageModel:avatar_thumbnail', AvatarThumbnail)


class MyImageModel(models.Model):
    image = models.ImageField(
        upload_to='images/',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])]
    )

    avatar_thumbnail = ImageSpecField(source='image',
                                      id='app:MyImageModel:avatar_thumbnail')
    thumbnail_width = models.PositiveIntegerField(default=200)
    thumbnail_height = models.PositiveIntegerField(default=200)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    thumbnail_400 = ImageSpecField(
        source='image',
        processors=[ResizeToFit(400)],
        format='JPEG',
        options={'quality': 90}
    )
    thumbnail_200 = ImageSpecField(
        source='image',
        processors=[ResizeToFit(200)],
        format='JPEG',
        options={'quality': 90}
    )






