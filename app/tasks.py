from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from .models import MyImageModel


@shared_task
def expire_link():
    print("dasdasdasd")
    return "dasdsadasd"
    # for obj in MyImageModel.objects.all():
    #     if obj.id == 51:
    #         obj.expiration_link = "test"
    #         obj.save()
    #     # if timezone.now() > obj.expiration_date:
    #     #     obj.expiration_link = None
    #     #     obj.save()
    #
    # return "compleated======="

