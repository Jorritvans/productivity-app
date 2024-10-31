from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import api_root, MyTokenObtainPairView
from tasks.views import CommentViewSet

# Router setup for Comment API
comment_router = DefaultRouter()
comment_router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),  # Account endpoints under /api/accounts/
    path('api/tasks/', include('tasks.urls')),        # Task endpoints under /api/tasks/
    path('api/', include(comment_router.urls)),       # Comment endpoints under /api/comments/
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', api_root, name='api_root'),              # Root view at the base URL
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
