from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Student
from .serializers import StudentSerializer
from classes.models import Class

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['current_class', 'is_active']
    search_fields = ['first_name', 'last_name', 'student_id', 'email']

    @action(detail=False, methods=['post'])
    def bulk_assign_class(self, request):
        """
        Bulk assign students to a class.
        Expected payload: { "student_ids": [1,2,3], "class_id": 5 }
        """
        student_ids = request.data.get('student_ids', [])
        class_id = request.data.get('class_id')

        if not student_ids or not class_id:
            return Response(
                {"error": "student_ids and class_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            target_class = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return Response(
                {"error": "Class not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        updated = Student.objects.filter(id__in=student_ids).update(current_class=target_class)

        return Response({
            "updated": updated,
            "message": f"{updated} students assigned to class {target_class.name}"
        })