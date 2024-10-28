# tasks/views.py

from rest_framework import viewsets, permissions, filters
from .models import Task, Comment  # Import Comment model
from .serializers import TaskSerializer, CommentSerializer  # Import CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
import logging
from django.contrib.auth.models import User

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
            # Assign the owner as the logged-in user
            task = serializer.save(owner=self.request.user)
            logger.info(f'Task created: {task.title} by {self.request.user}')
        except IntegrityError as e:
            logger.error(f'Error creating task: {str(e)}')
            raise e

    def get_queryset(self):
        """
        Override to filter the queryset so each user only sees their own tasks.
        """
        queryset = super().get_queryset().filter(owner=self.request.user)
        category = self.request.query_params.get('category', '')
        priority = self.request.query_params.get('priority', '')
        state = self.request.query_params.get('state', '')

        # Apply filters only if they are set and not blank
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

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def assign(self, request, pk=None):
        task = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            task.owners.add(user)
            return Response({'status': 'user assigned'})
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=400)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unassign(self, request, pk=None):
        task = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            task.owners.remove(user)
            return Response({'status': 'user unassigned'})
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=400)

# Add the custom permission class
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a comment to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the comment.
        return obj.author == request.user

# Update the CommentViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Optionally, filter comments by task if needed
    def get_queryset(self):
        queryset = super().get_queryset()
        task_id = self.request.query_params.get('task', None)
        if task_id is not None:
            queryset = queryset.filter(task_id=task_id)
        return queryset
