from django.contrib import admin

from .models import Author, Genre, Book, BookInstance, Language


class BooksInline(admin.TabularInline):
    # Authorの編集画面にbookも追加。
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Book
# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    # 管理画面に表示する項目。date_of_deathはmodels.pyで挙動が違う。
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # タップル()内のものは横に並べて表示される（横幅で変化する）
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]
# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    

# デコレータ(decorator)を使ってモデルを登録
# Register the Admin classes for Book using the decortor
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # 'genre'はManyToMayなのでDBにアクセス負荷ががかるため、使用しない。
    # 例；１つの本で100個のジャンルを持つ可能性もある。
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id', )
    # 検索フィルター
    list_filter = ('status', 'due_back')
    # 'Availability'のセクションを追加。
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

# Register your models here.
# それぞれのモデルに登録(register)できる。
#admin.site.register(Book)
#admin.site.register(Author)
#admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)
