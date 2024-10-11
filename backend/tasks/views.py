from rest_framework import viewsets, permissions, filters
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        # Automatically add the logged-in user as an owner
        task = serializer.save()
        task.owners.add(self.request.user)
    
    def get_queryset(self):
        # Filter tasks by the current user
        user = self.request.user
        queryset = self.queryset.filter(owners=user)

        # Get query parameters for filtering
        category = self.request.query_params.get('category')
        priority = self.request.query_params.get('priority')
        state = self.request.query_params.get('state')

        # Apply filtering based on the provided parameters
        if category:
            queryset = queryset.filter(category=category)
        if priority:
            queryset = queryset.filter(priority=priority)
        if state:
            queryset = queryset.filter(state=state)

        return queryset

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def assign(self, request, pk=None):
        # Assign another user to the task
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
        # Unassign a user from the task
        task = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            task.owners.remove(user)
            return Response({'status': 'user unassigned'})
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=400)
