"""
URL configuration for productivity_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import api_root  # Import your api_root view
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include your app URLs
    path('api/accounts/', include('accounts.urls')),
    path('api/tasks/', include('tasks.urls')),

    # JWT Token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Root URL - this will display the api_root view when you visit the root URL
    path('', api_root),  # This catches requests to the root URL
    
    # Browsable API authentication endpoints
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
