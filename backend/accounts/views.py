# accounts/views.py

from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    try:
        # Create user
        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({"message": "Registration successful."}, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response({"error": "Username or email already exists."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
