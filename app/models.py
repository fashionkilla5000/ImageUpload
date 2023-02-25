from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


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

