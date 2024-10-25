from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # Read-only owner field

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'state', 'due_date', 'priority', 'category', 'owner']  # Include 'owner'
