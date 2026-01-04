
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect,render

from blogs.models import Blog,Category
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
