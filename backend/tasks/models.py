from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=(('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')))
    category = models.CharField(max_length=50)
    state = models.CharField(max_length=50, choices=(('To-Do', 'To-Do'), ('In Progress', 'In Progress'), ('Done', 'Done')))
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class RelatedModel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f'Related to {self.task.title}'
