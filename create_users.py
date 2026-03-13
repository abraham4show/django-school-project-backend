from django.contrib.auth.models import User
from teachers.models import Teacher
from students.models import Student
from accounts.models import Profile   # if this app exists

# Create users for teachers
for teacher in Teacher.objects.filter(user__isnull=True):
    if teacher.email:
        username = teacher.email.split('@')[0]
    else:
        username = f"{teacher.first_name.lower()}.{teacher.last_name.lower()}".replace(' ', '')
    base = username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{counter}"
        counter += 1

    user = User.objects.create_user(
        username=username,
        email=teacher.email or '',
        password="changeme123",
        first_name=teacher.first_name,
        last_name=teacher.last_name
    )
    teacher.user = user
    teacher.save()
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.role = 'teacher'
    profile.teacher = teacher
    profile.save()
    print(f"Created user for teacher: {teacher.first_name} {teacher.last_name} (username: {username})")

# Create users for students
for student in Student.objects.filter(user__isnull=True):
    if student.email:
        username = student.email.split('@')[0]
    else:
        username = f"{student.first_name.lower()}.{student.last_name.lower()}".replace(' ', '')
    base = username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{counter}"
        counter += 1

    user = User.objects.create_user(
        username=username,
        email=student.email or '',
        password="changeme123",
        first_name=student.first_name,
        last_name=student.last_name
    )
    student.user = user
    student.save()
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.role = 'student'
    profile.student = student
    profile.save()
    print(f"Created user for student: {student.first_name} {student.last_name} (username: {username})")