from django.urls import path
from . import views

app_name = 'reviews'


urlpatterns = [
    path('search/books/', views.BookSearchView.as_view(), name='book_search'),
    path('books/', views.AllBooksView.as_view(), name='all_books'),
]