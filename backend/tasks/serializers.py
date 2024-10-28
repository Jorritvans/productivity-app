# tasks/serializers.py

from rest_framework import serializers
from .models import Task, Comment
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'state', 'due_date', 'priority', 'category', 'owner', 'comments']

    def get_comments(self, obj):
        comments = obj.comments.all()
        return CommentSerializer(comments, many=True, context=self.context).data

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    author = serializers.ReadOnlyField(source='author.id')  # Ensure author ID is an integer

    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'author_username', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at', 'author_username']
