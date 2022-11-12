from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Account, Relationship


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    # if the user is created, then create an associating account
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=Relationship)
def add_to_friends(sender, created, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    # if the status is accepted, add sender and receiver to each other's friend list
    if instance.status=='accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()

@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_from_friends(sender, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)
    sender.save()
    receiver.save()