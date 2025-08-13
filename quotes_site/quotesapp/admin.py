from django.contrib import admin
from .models import Author, Tag, Quote


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["fullname"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("author", "short_text")
    search_fields = ["text", "author__fullname", "tags__name"]
    filter_horizontal = ("tags",)

    def short_text(self, obj):
        return str(obj)
