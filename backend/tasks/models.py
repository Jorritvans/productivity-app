from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=(('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')))
    category = models.CharField(max_length=50, choices=(('Work', 'Work'), ('Personal', 'Personal'), ('Others', 'Others')))
    state = models.CharField(max_length=50, choices=(('To-Do', 'To-Do'), ('In Progress', 'In Progress'), ('Done', 'Done')))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tasks")

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.task.title}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  # Save the comment first

        if self.task.owner != self.author:  # Avoid self-notifications
            try:
                Notification.objects.create(
                    recipient=self.task.owner,
                    message=f"{self.author.username} {'commented on' if is_new else 'edited a comment on'} your task '{self.task.title}'"
                )
            except IntegrityError as e:
                print(f"Integrity error creating notification: {e}")
            except Exception as e:
                print(f"Unexpected error in notification creation: {e}")

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username}"

# Signal for handling comment deletion notification
@receiver(post_delete, sender=Comment)
def notify_comment_deleted(sender, instance, **kwargs):
    if instance.task.owner != instance.author:  # Avoid self-notifications
        try:
            Notification.objects.create(
                recipient=instance.task.owner,
                message=f"{instance.author.username} deleted a comment on your task '{instance.task.title}'"
            )
        except IntegrityError as e:
            print(f"Integrity error creating delete notification: {e}")
        except Exception as e:
            print(f"Unexpected error in delete notification creation: {e}")
