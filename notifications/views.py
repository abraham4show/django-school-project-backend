from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Notification
from .serializers import NotificationSerializer
from students.models import Student

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()  # Required for DRF
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only notifications for the logged-in user
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def send_to_all_students(self, request):
        title = request.data.get('title')
        message = request.data.get('message')
        link = request.data.get('link', '')
        event_date = request.data.get('event_date', None)
        notification_type = request.data.get('type', 'general')

        if not title or not message:
            return Response({'error': 'title and message are required'}, status=status.HTTP_400_BAD_REQUEST)

        students = Student.objects.filter(user__isnull=False).select_related('user')
        notifications = [
            Notification(
                recipient=s.user,
                title=title,
                message=message,
                link=link,
                type=notification_type,
                event_date=event_date
            )
            for s in students
        ]
        Notification.objects.bulk_create(notifications)
        return Response({'status': f'Notification sent to {len(notifications)} students'})