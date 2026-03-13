from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'current_class', 'is_active')
    list_filter = ('current_class', 'is_active', 'enrollment_date')
    search_fields = ('first_name', 'last_name', 'student_id', 'email')
    date_hierarchy = 'enrollment_date'
    
    # Remove enrollment_date from fieldsets since it's auto-added
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'student_id', 'email', 'date_of_birth')
        }),
        ('Academic Information', {
            'fields': ('current_class', 'is_active')  # Removed enrollment_date from here
        }),
        ('Contact Information', {
            'fields': ('parent_name', 'parent_phone', 'address')
        }),
    )
    readonly_fields = ('student_id',)  # Only student_id is readonly, remove enrollment_date