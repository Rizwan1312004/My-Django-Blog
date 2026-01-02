from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name = 'heading'),
    path('login/', views.LoginUser, name='login'),
    path('<int:category_id>/', views.CategoryBlogs, name='category_blogs'),
    path('<slug:slug>/', views.BlogDetail, name='blog_detail'),
]