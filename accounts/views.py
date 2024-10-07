from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer

# View to handle user registration
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Allow anyone to access this view
