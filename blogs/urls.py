from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name = 'heading'),
    path('register/', views.RegisterUser, name='register_user'),
    path('login/', views.LoginUser, name='login_user'),
    path('logout/', views.LogoutUser, name='logout_user'),
    path('search/', views.SearchResults, name='search_results'),
    path('<int:category_id>/', views.CategoryBlogs, name='category_blogs'),
    path('<slug:slug>/', views.BlogDetail, name='blog_detail'),
]