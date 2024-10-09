from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_date', 'priority', 'category', 'completed']
    list_filter = ['priority', 'category', 'completed']