from django.urls import path
from .views import UserListView, UserDetailView
from . import views

urlpatterns = [
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users/register/', views.register, name='register'),
    path('users/login/',views.user_login,name="login"),
    path('users/logout',views.user_logout,name="logout"),
    path('users/all_users',views.all_users,name="all_users"),
    path('users/view_user/<int:pk>',views.view_user,name="view_user"),
    path('users/delete_user/<int:pk>',views.delete_user,name="delete_user"),
]