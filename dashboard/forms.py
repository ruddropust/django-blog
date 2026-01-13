from django.forms import ModelForm
from django import forms
from blogs.models import Blog
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class AddBlogForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields = ['title','category','featured_image', 'short_description', 'blog_body', 'status', 'is_featured', 'is_slidePost']

class EditBlogForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields = ['title','category','author', 'featured_image', 'short_description', 'blog_body', 'status', 'is_featured', 'is_slidePost']



class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'is_active', 'is_staff','groups','user_permissions']

    def clean_email(self):
            email = self.cleaned_data.get('email')

            if User.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError(f"{email} This email is already registered.")

            return email