# productivity_app/urls.py

from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import api_root, MyTokenObtainPairView  # Import custom TokenObtainPairView
from tasks.views import CommentViewSet  # Import CommentViewSet

# Create a router for comments
comment_router = DefaultRouter()
comment_router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include your app URLs
    path('api/accounts/', include('accounts.urls')),
    path('api/tasks/', include('tasks.urls')),  # Tasks endpoints under /api/tasks/

    # Include comments router directly under /api/
    path('api/', include(comment_router.urls)),  # Now /api/comments/ is available

    # JWT Token endpoints
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Use custom TokenObtainPairView
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Use default TokenRefreshView

    # Root URL - this will display the api_root view when you visit the root URL
    path('', api_root),  # This catches requests to the root URL

    # Browsable API authentication endpoints
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
