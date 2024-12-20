from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)


urlpatterns = [
    path('', views.accounts_root, name='accounts_root'),
    path('register/', views.register, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('profile/', views.profile_view, name='profile'),
    path('search/', views.search_users, name='search_users'),
    path('<int:owner_id>/tasks/', views.user_tasks, name='user_tasks'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('followed_tasks/', views.followed_tasks, name='followed_tasks'),
    path('following/', views.following_list, name='following_list'),
]
