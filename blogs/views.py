from django.shortcuts import render, get_object_or_404
from .models import Category, Blog
# Create your views here.

def Home(request):
    categories = Category.objects.all()
    featured_blogs = Blog.objects.filter(is_featured=True, status='published').order_by('-created_at')
    posts = Blog.objects.filter(is_featured=False, status='published').order_by('-created_at')
    context = {
        'categories': categories,
        'featured_blogs': featured_blogs,
        'posts': posts,
        }
    return render(request, 'Home.html', context)

def CategoryBlogs(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)
    featured_blogs = Blog.objects.filter(category=category,is_featured=True, status='published',).order_by('-created_at')
    posts = Blog.objects.filter(category=category, is_featured=False, status='published').order_by('-created_at')
    context = {
        'categories': categories,
        'category': category,
        'cat_posts': posts,
        'featured_blogs': featured_blogs,
    }
    return render(request, 'Home.html', context)

def BlogDetail(request, slug):
    blog_post = get_object_or_404(Blog, slug=slug, status='published')
    related_blogs = Blog.objects.filter(category=blog_post.category, status='published',).order_by('-created_at').exclude(slug=blog_post.slug)
    context ={
        'blog_post': blog_post,
        'related_blogs': related_blogs,
    }
    return render(request, 'main.html', context)

def LoginUser(request):
    return render(request, 'login.html')