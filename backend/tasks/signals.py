from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Notification
from django.contrib.auth.models import User

@receiver(post_save, sender=Comment)
def notify_task_owner_on_comment(sender, instance, created, **kwargs):
    if created:
        task = instance.task
        message = f"{instance.author.username} commented on your task: '{task.title}'"
        Notification.objects.create(recipient=task.owner, message=message)
