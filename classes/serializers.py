# from django.db import router

# from rest_framework import serializers
# from .models import Class, Subject
# from teachers.models import Teacher

# class SubjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subject
#         fields = ['id', 'name', 'code', 'description']

# class ClassSerializer(serializers.ModelSerializer):
#     teacher_name = serializers.CharField(source='teacher.full_name', read_only=True)
#     subject_names = serializers.StringRelatedField(source='subjects', many=True, read_only=True)

#     class Meta:
#         model = Class
#         fields = [
#             'id', 'name', 'section', 'academic_year',
#             'teacher', 'teacher_name',
#             'subjects', 'subject_names',
#             'created_at', 'updated_at'
#         ]


from rest_framework import serializers
from .models import Subject, Class

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    subject_names = serializers.StringRelatedField(source='subjects', many=True, read_only=True)

    class Meta:
        model = Class
        fields = '__all__'