from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect,render

from blogapp.forms import RegistratonForm
from blogs.models import Blog,Category
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

# Create your views here.
def post_by_category(request, category_id):
    posts = Blog.objects.filter(status="Published",category=category_id)
    # try:
    #     category_name = Category.objects.get(id=category_id)
    # except:
        # return redirect('home')
    category_name = get_object_or_404(Category, id=category_id)
    # if the category doesnot exist use get_object_or_404 or try except block
    
    context = {
        'posts':posts,
        'category_name':category_name,
    }
    return render(request, 'post_by_category.html',context=context)

def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status="Published")

    context = {
        'single_blog':single_blog,
    }
    return render(request, 'blogs.html', context=context)
def search(request):
    keywords = request.GET.get('keyword')
    blogs = Blog.objects.filter(Q(title__icontains=keywords) | Q(short_description__icontains=keywords)| Q(blog_body__icontains=keywords), status="Published")

    context = {
        'blogs':blogs,
        'keywords':keywords,
    }
    return render(request, 'search.html', context=context)

def register(request):
    if request.method == "POST":
        fm = RegistratonForm(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect('home')
    else:
        fm = RegistratonForm()
    context = {
        "form":fm,
    }
    return render(request,'register.html', context)

def login(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request,request.POST)
        if fm.is_valid():
            username = fm.cleaned_data['username']
            password = fm.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')
    else:
        fm = AuthenticationForm()
    context={
        'form':fm
    }
    return render(request, 'login.html', context=context)

def logout_view(request):
    auth.logout(request)
    return redirect('home')
