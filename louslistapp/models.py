from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
# Create your models here.

class Course(models.Model):
    prof_name = models.CharField(max_length=100)
    prof_email = models.CharField(max_length=100)
    course_number = models.IntegerField(default=0)
    semester_code = models.IntegerField(default=0)
    course_section = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    catalog_number = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    units = models.CharField(max_length=100)
    component = models.CharField(max_length=100)
    class_capacity = models.IntegerField(default=0)
    waitlist = models.IntegerField(default=0)
    wait_cap = models.IntegerField(default=0)
    enrollment_total = models.IntegerField(default=0)
    enrollment_available = models.IntegerField(default=0)
    days = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    # is_favorited = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.description


class Instructor(models.Model):
    prof_name = models.CharField(max_length=100)
    prof_email = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.prof_name


# class Schedule(models.Model):
#     # Courses
#     courses = ArrayField(Course, size=8)
#     time_conflict = models.BooleanField()
#     comments = ArrayField(models.CharField(max_length=500), size=20)


# class Student(models.Model):
#     email = models.CharField(max_length=100)
#     schedules = ArrayField(Schedule, size=10)
#     favorites = ArrayField(Course, size=50)
    # friends = ArrayField(Student, size=10)
    # username?

# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     email = models.CharField(max_length=100)
#     @receiver(models.signals.post_save, sender=get_user_model())
#     def create_student_user(sender, instance, created, **kwargs):
#         if created:
#             Student.objects.create(user=instance)

class Schedule(models.Model):
    # Courses
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    credits = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default="Schedule 1")
    courses = models.ManyToManyField(Course, related_name="schedules")
    
    def __str__(self):
        return self.description
    

# class Profile(models.Model):
#     email = models.CharField(max_length=100)
#     username = models.CharField(max_length=100, default = "Guest")
#     schedules = models.ManyToManyField(Schedule, blank=True)