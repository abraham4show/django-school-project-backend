from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Profile
from teachers.models import Teacher
from students.models import Student

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)
    # For teacher/student, we might need additional fields to link to existing records
    # For simplicity, we'll create new Teacher/Student profiles on registration

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role')
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.save()
        # Create profile
        profile = Profile.objects.get(user=user)
        profile.role = role
        profile.save()

        # If role is teacher, create a Teacher record (optional, you might want to link to existing)
        if role == 'teacher':
            teacher = Teacher.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                # other fields can be filled later
            )
            profile.teacher = teacher
            profile.save()
        elif role == 'student':
            student = Student.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                # other fields can be filled later
            )
            profile.student = student
            profile.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role')
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role')