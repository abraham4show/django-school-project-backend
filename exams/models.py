from django.db import models
from classes.models import Class, Subject
from django.contrib.auth.models import User

class Exam(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='exams')
    date = models.DateField()
    duration = models.CharField(max_length=50)
    total_marks = models.IntegerField(default=0, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='exams_created')

    def __str__(self):
        return self.title

class Question(models.Model):
    TYPE_CHOICES = [
        ('mcq', 'Multiple Choice'),
        ('essay', 'Essay'),
        ('truefalse', 'True/False'),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    points = models.IntegerField(default=5)
    order = models.PositiveIntegerField(default=0)
    options = models.JSONField(blank=True, null=True)
    correct_answer = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.exam.title} - Q{self.order}"

class ExamAttempt(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='exam_attempts')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    passed = models.BooleanField(default=False)

class Answer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
    selected_option = models.CharField(max_length=255, blank=True)
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.FloatField(default=0)  # Removed trailing comma