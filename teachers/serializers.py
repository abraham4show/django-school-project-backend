from rest_framework import serializers
from .models import Teacher
from classes.models import Class

class TeacherSerializer(serializers.ModelSerializer):
    class_names = serializers.StringRelatedField(source='classes', many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'phone', 'address',
                  'qualification', 'employee_id', 'date_joined', 'is_active', 'classes', 'class_names']
        read_only_fields = ['employee_id', 'date_joined']