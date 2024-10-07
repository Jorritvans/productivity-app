from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Set up DRF's router for TaskViewSet
router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)

urlpatterns = [
    path('', views.index, name='index'),  # Root URL mapped to index view
    path('api/', include(router.urls)),   # API routes for TaskViewSet
]
