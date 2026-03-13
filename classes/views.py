from rest_framework import viewsets
from .models import Subject, Class
from .serializers import SubjectSerializer, ClassSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
@api_view(['GET'])
def subject_test(request):
    return Response({"message": "test ok"})


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def list(self, request, *args, **kwargs):
        print("🔥 SubjectViewSet.list called")
        return super().list(request, *args, **kwargs)