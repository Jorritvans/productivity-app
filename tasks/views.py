# tasks/views.py
from rest_framework import viewsets, permissions, filters
from .models import Task, Comment  # Removed Notification import
from .serializers import TaskSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
import logging
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

logger = logging.getLogger(__name__)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'priority', 'state']
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        try:
            task = serializer.save(owner=self.request.user)
            logger.info(f'Task created: {task.title} by {self.request.user}')
        except IntegrityError as e:
            logger.error(f'Error creating task: {str(e)}')
            raise e

    def get_queryset(self):
        queryset = super().get_queryset().filter(owner=self.request.user)
        category = self.request.query_params.get('category', '')
        priority = self.request.query_params.get('priority', '')
        state = self.request.query_params.get('state', '')

        if category:
            queryset = queryset.filter(category=category)
        if priority:
            queryset = queryset.filter(priority=priority)
        if state:
            queryset = queryset.filter(state=state)

        return queryset

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        try:
            return super().destroy(request, *args, **kwargs)
        except IntegrityError as e:
            logger.error(f'Error deleting task: {str(e)}')
            return Response({'error': 'Integrity error, foreign key constraint failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Removed notification logic

    def get_queryset(self):
        task_id = self.request.query_params.get('task', None)
        if task_id is not None:
            return self.queryset.filter(task_id=task_id)
        return self.queryset
