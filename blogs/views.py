from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Blog, Comments
from django.db.models import Q
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
    comments = Comments.objects.filter(blog=blog_post)
    if request.method == 'POST':
        update_comments = Comments()
        update_comments.writer = request.user
        update_comments.blog = blog_post
        update_comments.comment = request.POST.get('comment')
        update_comments.save()
    related_blogs = Blog.objects.filter(category=blog_post.category, status='published',).order_by('-created_at').exclude(slug=blog_post.slug)
    context ={
        'blog_post': blog_post,
        'related_blogs': related_blogs,
        'comments': comments,
    }
    return render(request, 'main.html', context)

def RegisterUser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_user')
        else:
            return render(request, "register.html", {"form": form})
    else: 
        register_form = RegisterForm()
        context = {
            'form': register_form,
        }
        return render(request, 'Register.html', context)

def LoginUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('heading')
    else:
        login_form = AuthenticationForm()
        context = {'form': login_form,}
        return render(request, 'Login.html', context)
    return render(request, 'Login.html', context)

    
def LogoutUser(request):
        logout(request)
        return redirect('heading')
        

def SearchResults(request):
    keyword = request.GET.get('keyword', '').strip()
    blog = None
    if keyword:
        blog = Blog.objects.filter(Q(title__icontains=keyword) | Q(blog_body__icontains=keyword) | Q(short_description__icontains=keyword), status='published').order_by('-created_at')
    context= {
            'keyword': keyword,
            'blog': blog,
        }
    return render(request, 'search.html', context)