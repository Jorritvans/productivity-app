# accounts/views.py

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
from .models import Following
from .serializers import FollowingSerializer

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
                "user_id": user.id,  # Include user_id in response
                "username": user.username,  # Include username in response
            }, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "Integrity error occurred"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User List View
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# Custom TokenObtainPairSerializer and TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['user_id'] = user.id  # Add user ID

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id  # Include user ID in response
        data['username'] = self.user.username
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# JWT Token Refresh View
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    try:
        followed_user = User.objects.get(id=user_id)
        if followed_user == request.user:
            return Response({'error': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        following_relation, created = Following.objects.get_or_create(follower=request.user, followed=followed_user)
        if not created:
            return Response({'error': 'You are already following this user.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': f'You are now following {followed_user.username}.'}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        followed_user = User.objects.get(id=user_id)
        following_relation = Following.objects.filter(follower=request.user, followed=followed_user)
        if following_relation.exists():
            following_relation.delete()
            return Response({'message': f'You have unfollowed {followed_user.username}.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not following this user.'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def followed_tasks(request):
    followed_users = Following.objects.filter(follower=request.user).values_list('followed', flat=True)
    tasks = Task.objects.filter(owner__id__in=followed_users)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def following_list(request):
    following_relations = Following.objects.filter(follower=request.user)
    followed_users = [relation.followed for relation in following_relations]
    serializer = UserSerializer(followed_users, many=True)
    return Response(serializer.data)
