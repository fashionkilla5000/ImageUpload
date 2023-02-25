from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from django.contrib.auth.models import User


class MyImageModel(models.Model):
    image = models.ImageField(upload_to='images/')
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
