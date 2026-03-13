from rest_framework import serializers
from .models import Student
from classes.models import Class

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name', 'section', 'academic_year']

class StudentSerializer(serializers.ModelSerializer):
    # Read-only fields for displaying class info
    class_name = serializers.CharField(source='current_class.name', read_only=True)
    class_section = serializers.CharField(source='current_class.section', read_only=True)
    
    # Write-only field for setting the class
    current_class_id = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(),
        source='current_class',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Student
        fields = [
            'id', 
            'student_id', 
            'first_name', 
            'last_name', 
            'email',
            'date_of_birth', 
            'current_class',
            'current_class_id',
            'class_name', 
            'class_section', 
            'parent_name', 
            'parent_phone',
            'address', 
            'is_active', 
            'enrollment_date', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['student_id', 'enrollment_date', 'created_at', 'updated_at']