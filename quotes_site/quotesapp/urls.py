from django.urls import path
from . import views


#  цей файл містить URL-шляхи для додатку quotesapp

app_name = "quotes" # Ім'я простору додатку для уникнення конфліктів імен URL

urlpatterns = [
    path("", views.index, name="index"), # Головна сторінка з усіма цитатами
    path("tag/<str:tag_name>/", views.tag_quotes, name="tag_quotes"), # Цитати за тегом
    path("author/<int:author_id>/", views.author_detail, name="author_detail"), # Деталі автора
    path("add-author/", views.add_author, name="add_author"), # Додавання нового автора
    path("add-quote/", views.add_quote, name="add_quote"), # Додавання нової цитати
]
