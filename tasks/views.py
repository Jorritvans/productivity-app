from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from django.http import HttpResponse


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

def index(request):
    return HttpResponse("Welcome to the Productivity App!")