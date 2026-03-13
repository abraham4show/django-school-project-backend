from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'first_name', 'last_name', 'email', 'is_active']
    list_filter = ['is_active']
    search_fields = ['first_name', 'last_name', 'email', 'employee_id']
    filter_horizontal = ['classes']
    fields = ['user', 'first_name', 'last_name', 'email', 'phone', 'address', 
              'qualification', 'employee_id', 'is_active', 'classes']