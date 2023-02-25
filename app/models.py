from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from django.contrib.auth.models import User
from django.conf import settings

from django.core.validators import FileExtensionValidator


class MyImageModel(models.Model):
    image = models.ImageField(
        upload_to='images/',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])]
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

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)

    def __str__(self):
        return "User: " + str(self.user) + ", Plan: " + str(self.plan)
