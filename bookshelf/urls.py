from django.urls import path

from . import views

# app_name = 'bookshelf'
urlpatterns = [
    path('', views.bookshelf_app, name='bs-homepage'),
    path('add/', views.add_book, name='add-book'),
    path('delete/', views.delete_book, name='delete-book'),
]

