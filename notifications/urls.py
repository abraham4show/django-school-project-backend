from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

router = DefaultRouter()
router.register(r'', NotificationViewSet, basename='notification')

print("Notification URLs:", [str(url) for url in router.urls])

urlpatterns = [
    path('', include(router.urls)),
]