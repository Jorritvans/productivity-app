from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        task = serializer.save()
        task.owners.add(self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(owners=user)
    
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
