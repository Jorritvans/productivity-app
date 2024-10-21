from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # JWT views

urlpatterns = [
    path('register/', views.register, name='register'),  # Register view
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT token refresh
    path('users/', views.UserListView.as_view(), name='user_list'),  # User list view
]
