from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamViewSet, ExamAttemptViewSet

router = DefaultRouter()
router.register(r'', ExamViewSet)  # exams at /api/exams/

urlpatterns = [
    path('attempts/', ExamAttemptViewSet.as_view({'get': 'list'}), name='attempt-list'),
    path('attempts/<int:pk>/submit/', ExamAttemptViewSet.as_view({'post': 'submit'}), name='attempt-submit'),
    path('<int:pk>/start/', ExamViewSet.as_view({'post': 'start'}), name='exam-start'),
    path('', include(router.urls)),
]

print("Exams router URLs:", [str(url) for url in router.urls])