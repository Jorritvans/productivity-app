from django.contrib import admin
from .models import Task, Comment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_date', 'priority', 'category', 'owner']
    list_filter = ['priority', 'category', 'state', 'owner']
    search_fields = ['title', 'description', 'owner__username']
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'task', 'created_at', 'content_summary']
    list_filter = ['author', 'task', 'created_at']
    search_fields = ['author__username', 'task__title', 'content']

    def content_summary(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_summary.short_description = 'Content'
