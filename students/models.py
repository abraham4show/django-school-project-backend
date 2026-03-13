from django.db import models
from django.contrib.auth.models import User
from classes.models import Class
import datetime


class Student(models.Model):
    # Personal Information
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='student_profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=20, unique=True, blank=True, editable=False, 
                                help_text="Auto-generated unique student ID")
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    
    # Academic Information
    current_class = models.ForeignKey(
        Class, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='students'
    )
    enrollment_date = models.DateField(auto_now_add=True)  # This is auto-added
    
    # Contact Information
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=20)
    address = models.TextField()
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.student_id:
            # Generate student_id in format: STU-YYYY-XXXX
            # Where YYYY is current year and XXXX is sequential number
            
            current_year = datetime.datetime.now().year
            
            # Get the last student created this year
            last_student = Student.objects.filter(
                student_id__startswith=f'STU-{current_year}-'
            ).order_by('student_id').last()
            
            if last_student and last_student.student_id:
                # Extract the sequential number from last student_id
                last_number = int(last_student.student_id.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            # Format with leading zeros (e.g., STU-2026-0001)
            self.student_id = f'STU-{current_year}-{new_number:04d}'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    class Meta:
        ordering = ['student_id']

        