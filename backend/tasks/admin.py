from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_date', 'priority', 'category', 'owner']  # Display 'owner'
    list_filter = ['priority', 'category', 'state', 'owner']  # Add 'owner' to filters
    search_fields = ['title', 'description', 'owner__username']  # Allow search by owner's username
