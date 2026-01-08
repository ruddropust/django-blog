from django.forms import ModelForm
from django import forms
from blogs.models import Blog


class AddBlogForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields = ['title','category','featured_image', 'short_description', 'blog_body', 'status', 'is_featured', 'is_slidePost']

class EditBlogForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields = ['title','category','author', 'featured_image', 'short_description', 'blog_body', 'status', 'is_featured', 'is_slidePost']