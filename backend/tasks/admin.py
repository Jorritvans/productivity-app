from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_date', 'priority', 'category', 'state']
    list_filter = ['priority', 'category', 'state']
    search_fields = ['title', 'description']
    filter_horizontal = ['owners']
