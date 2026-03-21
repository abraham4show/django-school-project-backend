from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Exam, Question, ExamAttempt, Answer
from .serializers import ExamSerializer, ExamAttemptSerializer
from accounts.permissions import IsTeacherOrAdmin, IsStudent

print("Loading exams/views.py")  # Debug print

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsTeacherOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [perm() for perm in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'profile') and user.profile.role == 'teacher':
                return Exam.objects.filter(created_by=user)
            elif hasattr(user, 'profile') and user.profile.role == 'student':
                student = getattr(user, 'student_profile', None)
                if student and student.current_class:
                    return Exam.objects.filter(status='published', class_group=student.current_class)
                return Exam.objects.none()
        return Exam.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsStudent])
    def start(self, request, pk=None):
        """Start an exam attempt for the student."""
        exam = self.get_object()
        if exam.status != 'published':
            return Response({'error': 'Exam is not published'}, status=status.HTTP_400_BAD_REQUEST)

        student = getattr(request.user, 'student_profile', None)
        if not student:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for ANY existing attempt (submitted or ongoing)
        existing = ExamAttempt.objects.filter(student=student, exam=exam).first()
        if existing:
            if existing.submitted_at:
                return Response({'error': 'You have already taken this exam.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Return the ongoing attempt
                serializer = ExamAttemptSerializer(existing)
                return Response(serializer.data, status=status.HTTP_200_OK)

        # Create new attempt
        attempt = ExamAttempt.objects.create(student=student, exam=exam)
        serializer = ExamAttemptSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ExamAttemptViewSet(viewsets.ModelViewSet):
    queryset = ExamAttempt.objects.none()
    serializer_class = ExamAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.role == 'student':
            return ExamAttempt.objects.filter(student=user.student_profile)
        return ExamAttempt.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            print("🔥 ERROR in ExamAttemptViewSet.list:")
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)

    @action(detail=False, methods=['post'], permission_classes=[IsStudent])
    def start(self, request):
        """Start an exam attempt (alternative method – not used by frontend)."""
        exam_id = request.data.get('exam_id')
        try:
            exam = Exam.objects.get(id=exam_id, status='published')
        except Exam.DoesNotExist:
            return Response({'error': 'Exam not found or not published'}, status=status.HTTP_404_NOT_FOUND)

        if ExamAttempt.objects.filter(student=request.user.student_profile, exam=exam, submitted_at__isnull=True).exists():
            return Response({'error': 'You already have an ongoing attempt'}, status=status.HTTP_400_BAD_REQUEST)

        attempt = ExamAttempt.objects.create(
            student=request.user.student_profile,
            exam=exam
        )
        serializer = self.get_serializer(attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit answers for an attempt."""
        attempt = self.get_object()
        if attempt.submitted_at:
            return Response({'error': 'Exam already submitted'}, status=status.HTTP_400_BAD_REQUEST)

        answers_data = request.data.get('answers', [])
        attempt.answers.all().delete()

        total_score = 0
        for ans in answers_data:
            question = Question.objects.get(id=ans['question'])
            is_correct = False
            marks = 0
            if question.type in ['mcq', 'truefalse']:
                is_correct = question.correct_answer == ans.get('answer_text', '')
                if is_correct:
                    marks = question.points
            Answer.objects.create(
                attempt=attempt,
                question=question,
                answer_text=ans.get('answer_text', ''),
                selected_option=ans.get('selected_option', ''),
                is_correct=is_correct,
                marks_obtained=marks
            )
            total_score += marks

        attempt.score = total_score
        attempt.passed = total_score >= (attempt.exam.total_marks * 0.5)
        attempt.submitted_at = timezone.now()
        attempt.save()

        return Response({'score': total_score, 'passed': attempt.passed})