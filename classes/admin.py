from django.contrib import admin
from .models import Class, Subject

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'academic_year', 'teacher']
    list_filter = ['section', 'academic_year']
    filter_horizontal = ['subjects']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']