from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('users/', views.UserListView.as_view(), name='user-list'),
]
