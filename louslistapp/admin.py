from django.contrib import admin
from .models import Course, Account, Relationship
# from .models import Schedule, Comment

# Register your models here.
admin.site.register(Course)
admin.site.register(Account)
admin.site.register(Relationship)
# admin.site.register(Schedule)
# admin.site.register(Comment)