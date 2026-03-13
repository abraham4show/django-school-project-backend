from rest_framework import serializers
from .models import AttendanceRecord
from students.models import Student
from classes.models import Class

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    class_name = serializers.CharField(source='class_obj.name', read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'student', 'student_name', 'student_id', 'class_obj', 'class_name', 'date', 'status', 'remarks', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        # Ensure the student belongs to the class (optional but good)
        student = data.get('student')
        class_obj = data.get('class_obj')
        if student and class_obj and student.class_field != class_obj:
            raise serializers.ValidationError("Student does not belong to this class.")
        return data