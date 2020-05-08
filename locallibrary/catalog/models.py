from django.db import models
# URLの正規表現のパターンからURLを逆生成する。
# Used to generate URLs by reversing the URL patterns
from django.urls import reverse
import uuid #Required for unique book instances

# Create your models here.
class Genre(model.Model):
    """Model representing a book genre."""
    # CharField 長さを指定するstrings
    # help_text 入力例などをHTMLのフォームに表示する。
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g Science Fiction)')

    # adminなどでクラスの中身を確認するために必要。
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = model.CharField(max_length=200)

    # authorは複数の本を書くが、本は一人の著者のみ→Foreign keyを使う。
    # Foreign Key used because book can only have one author, but authors can have multiplebooks
    # Authorはまだこのファイル内で宣言されていないので、stirngでなくobject
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = model.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CHarField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # genreは複数のbookを含む　bookも複数のジャンルをもつ→ManyToManyを使う。
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genreのクラスは上で定義されている。
    # Genre class has already been defined so we can specify the object above.
    genre =models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    