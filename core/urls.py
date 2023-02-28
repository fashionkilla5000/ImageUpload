from django.urls import include, path
from rest_framework import routers
from app import views
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'images', views.MyImageModelViewSet, basename='myimages')
router.register(r'subscription-plan', views.SubscriptionPlanViewSet)
router.register(r'user-subscription', views.UserSubscriptionViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
