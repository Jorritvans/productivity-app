from rest_framework import viewsets, permissions, filters
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
import logging

logger = logging.getLogger(__name__)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'priority', 'state']
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        try:
            task = serializer.save()
            logger.info(f'Task created: {task.title}')
        except IntegrityError as e:
            logger.error(f'Error creating task: {str(e)}')
            raise e

    def get_queryset(self):
        """
        Override to filter the queryset based on category, priority, and state.
        """
        queryset = super().get_queryset()
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
