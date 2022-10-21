import datetime
from email.policy import default
from msilib.schema import Component
from django.db import models
from django.utils import timezone
from django.contrib import admin
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
    wait_list = models.IntegerField(default=0)
    wait_cap = models.IntegerField(default=0)
    enrollment_total = models.IntegerField(default=0)
    enrollment_available = models.IntegerField(default=0)
    days = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.description

class Instructor(models.Model):
    prof_name = models.CharField(max_length=100)
    prof_email = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.prof_name
