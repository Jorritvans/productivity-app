from django.db import models, IntegrityError
from django.contrib.auth.models import User
import logging 

# Set up a logger
logger = logging.getLogger(__name__)

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
