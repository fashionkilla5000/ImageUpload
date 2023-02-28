from django.contrib import admin
from .models import MyImageModel, SubscriptionPlan, UserSubscription, ThumbnailSize


admin.site.register(ThumbnailSize)
admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscription)
admin.site.register(MyImageModel)

# Register your models here.
