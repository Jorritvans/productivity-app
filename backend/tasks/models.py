from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Task(models.Model):
    STATE_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    category = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='Open')
    attachment = CloudinaryField('attachment', blank=True, null=True)
    owners = models.ManyToManyField(User, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
