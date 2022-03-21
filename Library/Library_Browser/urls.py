from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('authors/', views.authors_home, name='authors_home'),
    path('authors/<int:pk>/', views.author_detail, name='author_detail'),
    
    path('books/', views.books_home, name='books_home'),
    path('books/<int:pk>/', views.book_detail, name='book_detail')
]