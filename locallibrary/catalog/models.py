import uuid #Required for unique book instances
from django.db import models
# URLの正規表現のパターンからURLを逆生成する。
# Used to generate URLs by reversing the URL patterns
from django.urls import reverse


# Create your models here.
class Genre(models.Model):
    """Model representing a book genre."""
    # CharField 長さを指定するstrings
    # help_text 入力例などをHTMLのフォームに表示する。
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g Science Fiction)')



    # adminなどでクラスの中身を確認するために必要。
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Language(models.Model):
    """Model representing a Language (e.g. English, French etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural Language (e.g. English, French etc.)")     
    def __str__(self):
        """String for representing the Model object  (in Admin site etc.)"""
        return self.name

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    # authorは複数の本を書くが、本は一人の著者のみ→Foreign keyを使う。
    # Foreign Key used because book can only have one author, but authors can have multiplebooks
    # Authorはまだこのファイル内で宣言されていないので、stirngでなくobject
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # genreは複数のbookを含む　bookも複数のジャンルをもつ→ManyToManyを使う。
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genreのクラスは上で定義されている。
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admim."""
        # はじめから3のジャンルをくっつけて表示する。
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

# 本1冊の詳細
class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    # UUIDField primary_key for this model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    # bookは複数のcopyをもつが、copyはbookのみ→ForeignKey(同じ本が複数あるイメージ)
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    # impirnt は出版社？
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        # 棚にないと貸し出せないため
        default='m',
        help_text='BOOK availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing thme Model object."""
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'