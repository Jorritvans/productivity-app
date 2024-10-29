from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, user_notifications
from . import views

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('notifications/', user_notifications, name='user_notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_as_read, name='mark_notification_as_read'),
]
