from django.shortcuts import render
from django.views import generic
# ビューで使用するモデルのクラスをインポート
from catalog.models import Book, Author, BookInstance, Genre

# Create your views here.
def index(request):
    """View function for home page of site."""

    # レコードの数をフェッチ(fetch)する。
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # 利用可能な本の数を取得する。
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # SFを含む本の数
    num_genre_sf = Genre.objects.filter(name__exact='SF').count()
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre_sf': num_genre_sf,
        'num_visits': num_visits,
    }
    # HTMLページを生成して、responseとしてページを返す。
    # request HttpRequest
    # HTML template のプレースホルダ(placeholders)
    # context python 辞書  
    # Render the HTML template index.html with the data in the contex variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    #1ページごとに表示する数。
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model = Author

