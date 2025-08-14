from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F

from .models import Quote, Tag, Author
from .forms import AuthorForm, QuoteForm


# Головна сторінка з цитатами та пагінацією
def index(request):
    # список цитат (бачуть всі) + пагинація
    quotes = Quote.objects.select_related("author").prefetch_related("tags").all()
    paginator = Paginator(quotes, 10) # 10 цитат на сторінку
    page_number = request.GET.get("page") # Отримуємо номер сторінки з GET параметра
    page_obj = paginator.get_page(page_number)  # Отримуємо об'єкт сторінки з цитатами

    # ТОП-10 на кліки (глобальний)
    top_tags = Tag.objects.order_by("-click_count")[:10]

    # top_tags = get_top_tags()

    return render(
        request,
        "quotesapp/index.html", # Шаблон для головної сторінки
        {
            "page_obj": page_obj, # Об'єкт сторінки з цитатами
            "top_tags": top_tags, # ТОП-10 тегів на кліки
        },
    )


# ТОП 10 tags
def get_top_tags(limit=10):
    return Tag.objects.annotate(cnt=Count("quotes")).order_by("-cnt")[:limit]  


# Сторінка з цитатами за тегом
# @login_required
def tag_quotes(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name) # Отримуємо тег за його ім'ям

    # Збільшуємо лічильник кліків
    tag.click_count = F("click_count") + 1 # Використовуємо F-вираз для атомарного оновлення
    tag.save(update_fields=["click_count"]) # Зберігаємо зміни в базі даних
    tag.refresh_from_db()  # Щоб отримати оновлене значення
 
    # Отримуємо цитати з цим тегом, з автором та тегами
    quotes = (
        Quote.objects.filter(tags=tag).select_related("author").prefetch_related("tags") 
    )
    paginator = Paginator(quotes, 10) # 10 цитат на сторінку
    page_number = request.GET.get("page") # Отримуємо номер сторінки з GET параметра
    page_obj = paginator.get_page(page_number) # Отримуємо об'єкт сторінки з цитатами

    # Отримуємо ТОП-10 тегів на кліки, глобально для сайту
    top_tags = Tag.objects.order_by("-click_count")[:10]

    return render(
        request,
        "quotesapp/tag_quotes.html", # Шаблон для сторінки з цитатами за тегом
        {
            "page_obj": page_obj, # Об'єкт сторінки з цитатами за тегом
            "top_tags": top_tags,   # ТОП-10 тегів на кліки
            "current_tag": tag, # Поточний тег, за яким фільтруємо цитати
        },
    )


# Сторінка з цитатами за автором
# @login_required
def author_detail(request, author_id: int):
    author = get_object_or_404(Author, pk=author_id) # Отримуємо автора за його ID
    return render(
        request,
        "quotesapp/author_detail.html",  # Шаблон для сторінки з цитатами автора
        {"author": author, "hide_sidebar": True}, # Передаємо автора та приховуємо бічну панель
    )


# Додати автора (форми)
@login_required
def add_author(request):
    if request.method == "POST": # Якщо метод запиту POST (форма була відправлена)
        form = AuthorForm(request.POST) # Створюємо форму з даними POST
        if form.is_valid(): # Якщо форма валідна
            form.save() # Зберігаємо автора
            return redirect("quotes:index") # Перенаправляємо на головну сторінку з цитатами
    else:
        form = AuthorForm() # Якщо форма не була відправлена, створюємо порожню форму
    return render(request, "quotesapp/add_author.html", {"form": form}) # Шаблон для додавання автора   


# Додати цитату (форма)
@login_required
def add_quote(request):
    if request.method == "POST":  # Якщо метод запиту POST (форма була відправлена)
        form = QuoteForm(request.POST) # Створюємо форму з даними POST
        if form.is_valid(): # Якщо форма валідна
            form.save() # Зберігаємо цитату
            return redirect("quotes:index") # Перенаправляємо на головну сторінку з цитатами
    else:
        form = QuoteForm() # Якщо форма не була відправлена, створюємо порожню форму
    return render(request, "quotesapp/add_quote.html", {"form": form}) # Шаблон для додавання цитати
