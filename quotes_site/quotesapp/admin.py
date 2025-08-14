from django.contrib import admin
from .models import Author, Tag, Quote


# клас для керування авторами в адмінці
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["fullname"]  # пошук за повним ім'ям автора

# клас для управління тегами в адмінці
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["name"]

# клас для управління цитатами в адмінці
@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("author", "short_text")  # відображення автора та короткої цитати
    search_fields = [
        "text",
        "author__fullname",
        "tags__name",
    ]  # пошук по тексту цитати, повному імені автора та тегам
    filter_horizontal = ("tags",)  # горизонтальний фільтр для тегів

    # метод для відображення короткої цитати у списку
    def short_text(self, obj):
        return str(obj)
