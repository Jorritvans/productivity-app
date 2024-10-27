from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import UserSerializer
import logging
from tasks.models import Task
from tasks.serializers import TaskSerializer
from django.utils.dateformat import format
from datetime import datetime
from django.contrib.auth.models import User
from tasks.models import Task

logger = logging.getLogger(__name__)

# Simple API Root
@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        "accounts": "/api/accounts/",
        "tasks": "/api/tasks/",
        "token": "/api/token/",
        "refresh_token": "/api/token/refresh/",
    })

# User Registration View
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already in use"}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already in use"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate password
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Registration successful.",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "Integrity error occurred"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User List View
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# JWT Token views from `rest_framework_simplejwt`
MyTokenObtainPairView = TokenObtainPairView
MyTokenRefreshView = TokenRefreshView

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user

    # Retrieve user data
    user_data = {
        "username": user.username,
        "email": user.email,
        "date_joined": user.date_joined.strftime("%Y-%m-%d"),  # Format date here
    }

    # Retrieve tasks associated with the user
    tasks = Task.objects.filter(owner=user)
    task_data = TaskSerializer(tasks, many=True).data

    return Response({
        "user": user_data,
        "tasks": task_data,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    query = request.query_params.get('q', '')  # Get the 'q' parameter from the query string
    users = User.objects.filter(username__icontains=query)  # Filter users by username containing the query string
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_tasks(request, owner_id):
    tasks = Task.objects.filter(owner_id=owner_id)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)