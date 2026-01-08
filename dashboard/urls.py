from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    #Category Crud
    path('categories/', views.categories, name='categories'),
    path('categories/delete/<int:id>/', views.delete_category, name='delete_category'),
    path('categories/edit/<int:id>/', views.edit_category, name='edit_category'),
    path('categories/add/', views.add_category, name='add_category'),

    #Blogpost Crud
    path('posts/', views.posts, name='posts'),
    path('posts/add/', views.add_post, name='add_post'),
    path('posts/edit/<int:id>/', views.edit_post, name='edit_post'),
    path('posts/delete/<int:id>/', views.delete_post, name='delete_post'),

]
