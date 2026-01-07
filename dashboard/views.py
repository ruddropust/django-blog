from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from blogs.models import Blog,Category
from django.contrib import messages

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    blog_count = Blog.objects.all().count()
    categories_count = Category.objects.all().count()
    context={
        'blog_count':blog_count,
        'categories_count':categories_count,
    }
    return render(request, 'dashboard.html', context=context)

def categories(request):
    categories = Category.objects.all().order_by('-created_at')
    context = {'categories': categories}
    return render(request, 'categories.html', context)

def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')

        if category_name:
            # case-insensitive check
            if Category.objects.filter(category_name__iexact=category_name).exists():
                messages.error(request, "Category already exists!")
                return redirect('categories')
            else:
                Category.objects.create(category_name=category_name)
                messages.success(request, "Category added successfully!")
        else:
            messages.error(request, 'Category name is required.')
            return redirect('categories')
    return redirect('categories')




def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully!")
    
    return redirect('categories')


def edit_category(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == 'POST':
        category_name = request.POST.get('category_name', '').strip()

        if not category_name:
            messages.error(request, 'Category name cannot be empty.')
            return redirect('categories')

        # If same as current name
        if category_name.lower() == category.category_name.lower():
            messages.error(request, 'Category name is the same as before.')
            return redirect('categories')

        # Check if another category already has this name
        if Category.objects.filter(category_name__iexact=category_name).exclude(id=category.id).exists():
            messages.error(request, 'Another category with this name already exists.')
            return redirect('categories')

        category.category_name = category_name
        category.save()
        messages.success(request, 'Category name updated successfully!')

    return redirect('categories')


def post(request):
    return render(request, 'post.html')