from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Teacher
from .serializers import TeacherSerializer
from classes.models import Class

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['first_name', 'last_name', 'email', 'employee_id']

    @action(detail=False, methods=['post'])
    def bulk_assign_to_class(self, request):
        """
        Assign multiple teachers to one class.
        Payload: { "teacher_ids": [1,2,3], "class_id": 5 }
        """
        teacher_ids = request.data.get('teacher_ids', [])
        class_id = request.data.get('class_id')

        if not teacher_ids or not class_id:
            return Response(
                {"error": "teacher_ids and class_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            target_class = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return Response(
                {"error": "Class not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        teachers = Teacher.objects.filter(id__in=teacher_ids)
        for teacher in teachers:
            teacher.classes.add(target_class)

        return Response({
            "assigned": len(teachers),
            "message": f"{len(teachers)} teachers assigned to class {target_class.name}"
        })

    @action(detail=True, methods=['post'])
    def assign_classes(self, request, pk=None):
        """
        Assign multiple classes to a specific teacher.
        URL: /api/teachers/{id}/assign_classes/
        Payload: { "class_ids": [1,2,3] }
        """
        teacher = self.get_object()
        class_ids = request.data.get('class_ids', [])

        if not class_ids:
            return Response(
                {"error": "class_ids are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        classes = Class.objects.filter(id__in=class_ids)
        teacher.classes.add(*classes)

        return Response({
            "assigned": len(classes),
            "message": f"{len(classes)} classes assigned to teacher {teacher.first_name} {teacher.last_name}"
        })