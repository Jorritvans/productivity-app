from django.db import models
from django.contrib.auth.models import User

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

class RelatedModel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f'Related to {self.task.title}'
