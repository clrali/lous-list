from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.db.models import Q
from django.db.models.signals import post_save
# Create your models here.

class Course(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
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
    start_time = models.CharField(max_length=100, default=None)
    end_time = models.CharField(max_length=100, default=None)
    location = models.CharField(max_length=100)
    selected = models.BooleanField(default=False)

    def __str__(self) -> str:
        # return self.start_time + " " + self.end_time
        return self.description


class Instructor(models.Model):
    prof_name = models.CharField(max_length=100)
    prof_email = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.prof_name

class AccountManager(models.Manager):

    def get_all_profiles_to_invite(self, sender):
        accounts = Account.objects.all().exclude(user=sender)
        account = Account.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=account) | Q(receiver=account))
        print(qs)
        
        # list of all accepted friend invitations
        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print("accepted friends: ", accepted)

        # list of all available profiles to invite
        available = [account for account in accounts if account not in accepted]
        print("available accounts: ", available)
        return available

    def get_all_profiles(self, me):
        # get all profiles except for your own
        accounts = Account.objects.all().exclude(user=me)
        return accounts

class Account(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    courses = models.ManyToManyField(Course, related_name='courses', blank=True)

    objects = AccountManager()

    def get_friends(self):
        return self.friends.all()
    
    def get_friends_count(self):
        return self.friends.all().count()
    
    def get_courses(self):
        return self.courses.all()
    
    def get_course_count(self):
        return self.courses.all().count()

    def __str__(self):
        return str(self.user)

# name on left is for database, name on right is human-readable in admin 
STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted'),
)

class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs
    

class Relationship(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    objects = RelationshipManager()

    def __str__(self) -> str:
        return f"{self.sender}-{self.receiver}-{self.status}"