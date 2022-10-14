from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class Course(models.Model):
    subject = models.CharField(max_length=50, blank=True)
    className = models.CharField(max_length=50, blank=True)
    professor = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.className