from django.shortcuts import render, redirect, get_object_or_404
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import CategoryForm


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
def category_list(request):
    categories = Category.objects.annotate(totel_posts=Count('blog'))
   
    context = {
        'categories': categories,
        }
    return render(request, 'dashboard/category.html', context)

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