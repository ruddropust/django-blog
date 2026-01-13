from django.contrib import admin
from .models import Category, Blog, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','category_name', 'created_at', 'updated_at']

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ['title', 'category', 'author', 'status', 'is_featured', 'is_slidePost']
    search_fields = ['id','title', 'category__category_name', 'author__username',  'status']
    list_editable=['status', 'is_featured','is_slidePost']


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)