from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register the ClassViewSet (empty prefix for /classes/)
router = DefaultRouter()
router.register(r'', views.ClassViewSet)  # handles /classes/ and /classes/<id>/

urlpatterns = [
    # Explicit path for subjects – bypasses router to avoid conflicts
    path('subjects/', views.SubjectViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='subject-list'),
    # Include all router-generated URLs for classes
    path('', include(router.urls)),
]