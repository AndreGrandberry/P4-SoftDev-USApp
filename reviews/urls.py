from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/books/', views.BookSearchView.as_view(), name='book_search'),
    path('books/', views.AllBooksView.as_view(), name='all_books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/<int:pk>/review/new/', views.CreateReviewView.as_view(), name='create_review'),
    path('book/<int:pk>/review/<int:review_id>/delete/', views.DeleteReviewView.as_view(), name='delete_review'),
    path('book/<int:pk>/review/<int:review_id>/edit/', views.EditReviewView.as_view(), name='edit_review'),
    path('book/new/', views.CreateBookView.as_view(), name='create_book'),
    path('all/', views.AllReviewsView.as_view(), name='reviews'),
]