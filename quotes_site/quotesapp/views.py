from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F

from .models import Quote, Tag, Author
from .forms import AuthorForm, QuoteForm


def index(request):
    # список цитат (бачуть всі) + пагинація
    quotes = Quote.objects.select_related("author").prefetch_related("tags").all()
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # ТОП-10 на кліки (глобальний)
    top_tags = Tag.objects.order_by("-click_count")[:10]

    # top_tags = get_top_tags()

    return render(
        request,
        "quotesapp/index.html",
        {
            "page_obj": page_obj,
            "top_tags": top_tags,
        },
    )


# ТОП 10 tags
def get_top_tags(limit=10):
    return Tag.objects.annotate(cnt=Count("quotes")).order_by("-cnt")[:limit]


# @login_required
def tag_quotes(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)

    # Збільшуємо лічильник кліків
    tag.click_count = F("click_count") + 1
    tag.save(update_fields=["click_count"])
    tag.refresh_from_db()  # Щоб отримати оновлене значення

    quotes = (
        Quote.objects.filter(tags=tag).select_related("author").prefetch_related("tags")
    )
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Отримуємо ТОП-10 тегів на кліки, глобально для сайту
    top_tags = Tag.objects.order_by("-click_count")[:10]

    return render(
        request,
        "quotesapp/tag_quotes.html",
        {
            "page_obj": page_obj,
            "top_tags": top_tags,
            "current_tag": tag,
        },
    )


# @login_required
def author_detail(request, author_id: int):
    author = get_object_or_404(Author, pk=author_id)
    return render(
        request,
        "quotesapp/author_detail.html",
        {"author": author, "hide_sidebar": True},
    )


@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("quotes:index")
    else:
        form = AuthorForm()
    return render(request, "quotesapp/add_author.html", {"form": form})


@login_required
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("quotes:index")
    else:
        form = QuoteForm()
    return render(request, "quotesapp/add_quote.html", {"form": form})
