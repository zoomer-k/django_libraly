from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    # classベースのview
    path('books/', views.BookListView.as_view(), name='books'),
    # caputure book iD pk(primary key)
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]