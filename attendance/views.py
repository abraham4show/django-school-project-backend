from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from .models import AttendanceRecord
from .serializers import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by query parameters
        class_id = self.request.query_params.get('class')
        date = self.request.query_params.get('date')
        student_id = self.request.query_params.get('student')

        if class_id:
            queryset = queryset.filter(class_obj_id=class_id)
        if date:
            parsed_date = parse_date(date)
            if parsed_date:
                queryset = queryset.filter(date=parsed_date)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset

    @action(detail=False, methods=['post'])
    def mark_bulk(self, request):
        """
        Bulk mark attendance for a class on a given date.
        Expects: { class_id: int, date: "YYYY-MM-DD", records: [ {student_id, status, remarks?} ] }
        """
        class_id = request.data.get('class_id')
        date_str = request.data.get('date')
        records = request.data.get('records', [])

        if not class_id or not date_str or not records:
            return Response({'error': 'class_id, date, and records are required'}, status=status.HTTP_400_BAD_REQUEST)

        date = parse_date(date_str)
        if not date:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        created = []
        updated = []
        errors = []

        for item in records:
            student_id = item.get('student_id')
            status_val = item.get('status')
            remarks = item.get('remarks', '')

            if not student_id or not status_val:
                errors.append({'student_id': student_id, 'error': 'student_id and status are required'})
                continue

            # Try to get or create attendance record for that student and date
            record, created_flag = AttendanceRecord.objects.update_or_create(
                student_id=student_id,
                date=date,
                defaults={
                    'class_obj_id': class_id,
                    'status': status_val,
                    'remarks': remarks
                }
            )
            if created_flag:
                created.append(record.id)
            else:
                updated.append(record.id)

        return Response({
            'created': created,
            'updated': updated,
            'errors': errors
        }, status=status.HTTP_200_OK)