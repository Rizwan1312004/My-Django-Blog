from django.shortcuts import render, redirect, get_object_or_404
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import CategoryForm, BlogForm, UserForm, UserEditForm
from django.contrib.auth.models import User


# Create your views here.
@login_required(login_url='login_user')
def dashboard(request):
    totel_posts = Blog.objects.all().order_by('-created_at')
    totel_categories = Category.objects.all().count()
    context = {
        'totel_posts': totel_posts,
        'totel_categories': totel_categories,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url='login_user')
def users(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'dashboard/users.html', context)

@login_required(login_url='login_user')
def add_users(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()

    return render(request, 'dashboard/user_add.html', {'form': form})

@login_required(login_url='login_user')
def edit_users(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    user = get_object_or_404(User, pk=pk)
    form = UserEditForm(instance=user)
    return render(request, 'dashboard/user_edit.html', {'form': form, 'user': user})

def delete_users(request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect('user_list')

@login_required(login_url='login_user')
def category_list(request):
    categories = Category.objects.annotate(totel_posts=Count('blog'))
   
    context = {
        'categories': categories,
        }
    return render(request, 'dashboard/category.html', context)

@login_required(login_url='login_user')
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/category_add.html', context)

@login_required(login_url='login_user')
def category_edit(request, pk):
    if request.method == 'POST':
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(instance=category)
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'dashboard/category_edit.html', context)

@login_required(login_url='login_user')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('category_list')

@login_required(login_url='login_user')
def post_list(request):
    search_query = request.GET.get('q', '').strip()
    posts = Blog.objects.filter(author=request.user)
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    pablised_posts = posts.filter(status='published').count()
    draft_posts = posts.filter(status='draft').count() 
    
    context = {
            'published_posts': pablised_posts,
            'draft_posts': draft_posts,
            'posts': posts,
        }
    return render(request, 'dashboard/posts.html', context)

@login_required(login_url='login_user')
def post_add(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('post_list')
    form = BlogForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/post_add.html', context)

@login_required(login_url='login_user')
def post_edit(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Blog, pk=pk)
        form = BlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('post_list')
    post = get_object_or_404(Blog, pk=pk)
    form = BlogForm(instance=post)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'dashboard/post_edit.html', context)

@login_required(login_url='login_user')
def post_delete(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('post_list')