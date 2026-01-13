from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from blogs.models import Blog,Category
from django.contrib import messages
from django.template.defaultfilters import slugify
from dashboard.forms import AddBlogForm,EditBlogForm, AddUserForm
from django.utils.text import slugify
from aboutus.admin import CustomUserAdmin
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

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



# POst app
def posts(request):
    posts = Blog.objects.all().order_by('updated_at').reverse()


    context={
        'posts':posts,
    }
    return render(request, 'posts.html',context)




def add_post(request):
    if request.method == 'POST':
        fm = AddBlogForm(request.POST, request.FILES)
        if fm.is_valid():
            post = fm.save(commit=False)
            post.author = request.user

            # Generate unique slug
            base_slug = slugify(post.title)
            slug = base_slug
            counter = 1

            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            post.slug = slug
            post.save()  # single save
            messages.success(request, "Post added successfully!")
            return redirect('posts')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        fm = AddBlogForm()

    context = {
        'form': fm,
        'page_title': 'Add New Post',
        'button_text': 'Save Post'
    }
    return render(request, 'add_post.html', context)



def edit_post(request, id):
    post = get_object_or_404(Blog, id=id)
    
    if request.method == 'POST':
        form = EditBlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.author = request.user
            updated_post.slug = slugify(updated_post.title)
            updated_post.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('posts')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditBlogForm(instance=post)

    context = {
        'form': form,
        'post': post,
        'page_title': 'Edit Post',
        'button_text': 'Update Post'
    }

    return render(request, 'edit_post.html', context)


def delete_post(request, id):
    post = get_object_or_404(Blog, pk=id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect('posts')
    return redirect('posts')


# Users
def users(request):
    User = get_user_model()
    if request.user.is_superuser:
        users = User.objects.filter(is_superuser=False).prefetch_related('groups')
    else:
        users = User.objects.filter(is_superuser=False).exclude(
                groups__name='manager').prefetch_related('groups')

    for user in users:
        print(", ".join(user.groups.values_list('name', flat=True)))

    context = {'users': users}
    return render(request, 'users.html', context)

def delete_user(request, id):
    user = get_user_model().objects.get(id=id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect('users')


def edit_user(request, id):
    User = get_user_model()
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        user_name = request.POST.get('user_name', '').strip()
        user_email = request.POST.get('user_email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if User.objects.filter(username__iexact=user_name).exclude(id=user.id).exists():
            messages.warning(request, user_name+' Username already taken')

        elif User.objects.filter(email__iexact=user_email).exclude(id=user.id).exists():
            messages.warning(request, user_email+' Email already taken')

        else:
            try:
                validate_email(user_email)

                user.username = user_name
                user.email = user_email
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                messages.success(request, 'User updated successfully')
                return redirect('users')

            except ValidationError:
                messages.error(request, user_email+' Invalid email address')

    return redirect('users')

def add_user(request):
    User = get_user_model()
    if request.method == 'POST':
        fm = AddUserForm(request.POST)
        
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Sucessfully added user...')
            return redirect('users')
    else:
        fm = AddUserForm()
    context = {
        'form':fm
    }
    return render(request, 'add_user.html', context)
