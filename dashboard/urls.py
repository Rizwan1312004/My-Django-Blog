from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/add/', views.post_add, name='post_add'),
    path('posts/edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('posts/delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('users/', views.users , name='user_list'),
    path('users/add', views.add_users , name='user_add'),
    path('users/edit/<int:pk>/', views.edit_users , name='user_edit'),
    path('users/delete/<int:pk>/', views.delete_users , name='user_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),

]
