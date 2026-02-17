from django.views.generic import ListView
from django.db.models import Avg, Count
from .models import Book

class BookSearchView(ListView):
    """
    List view for searching books by title.

    The search query is passed as a GET parameter `q`.
    """
    model = Book
    template_name = 'reviews/book_search_results.html'
    context_object_name = 'books'

    def get_queryset(self):
        """Return books matching the search query `q`

        (case-insensitive, partial match).

        """
        q = self.request.GET.get('q', '').strip()
        if not q:
            return Book.objects.none()
        return (
            Book.objects.filter(title__icontains=q)
            .order_by('title')
            .annotate(avg_rating=Avg('review__rating'), reviews_count=Count('review'))
        )


class AllBooksView(ListView):
    """List view for all books (paginated by title)."""
    model = Book
    template_name = 'reviews/all_books.html'
    context_object_name = 'books'
    queryset = Book.objects.all().order_by('title')
    paginate_by = 12
