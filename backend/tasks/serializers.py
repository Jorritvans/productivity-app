from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    owners = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'due_date',
            'priority',
            'category',
            'state',
            'attachment',
            'owners',
            'created_at',
            'updated_at',
        ]
