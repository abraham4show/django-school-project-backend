from django.contrib import admin
from .models import Exam, Question

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'class_group', 'date', 'status']
    list_filter = ['status', 'subject', 'class_group']
    inlines = [QuestionInline]