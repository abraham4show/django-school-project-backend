from django.db import models
from teachers.models import Teacher  # import Teacher from the teachers app

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True, unique=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Class(models.Model):
    SECTION_CHOICES = [
        ('Kindergarten', 'Kindergarten'),
        ('Nursery', 'Nursery'),
        ('Primary', 'Primary'),
    ]

    name = models.CharField(max_length=50)  # e.g., "kg 2", "pry 4"
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    academic_year = models.CharField(max_length=9, blank=True)  # e.g., "2025/2026"
    teacher = models.ForeignKey(
    'teachers.Teacher', on_delete=models.SET_NULL, null=True, blank=True,
    related_name='classes_taught'
)
    subjects = models.ManyToManyField(Subject, related_name='classes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Classes'
        ordering = ['section', 'name']

    def __str__(self):
        return f"{self.get_section_display()} - {self.name}"