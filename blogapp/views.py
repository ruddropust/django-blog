from django.shortcuts import redirect,render
from blogs.models import Blog, Category

def home(request):

    featured_post = Blog.objects.filter(is_featured=True, status='Published')
    slide_post = Blog.objects.filter(is_slidePost=True,status="Published").order_by('updated_at').reverse()
    posts = Blog.objects.filter(is_slidePost=False,is_featured=False,status="Published")
    context = {
        'featured_post':featured_post,
        'slide_post':slide_post,
        'posts':posts,
        }
    return render(request, 'home.html', context=context)