from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('categories/', views.categories, name='categories'),
    path('post/', views.post, name='post'),
    path('categories/delete/<int:id>/', views.delete_category, name='delete_category'),
    path('categories/edit/<int:id>/', views.edit_category, name='edit_category'),
    path('categories/add/', views.add_category, name='add_category'),

]
