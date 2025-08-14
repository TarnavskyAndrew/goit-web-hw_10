import json
from pathlib import Path
from django.core.management.base import BaseCommand
from quotesapp.models import Author, Tag, Quote

# клас Command для імпорту авторів та цитат з JSON файлів
class Command(BaseCommand):
    help = "Load authors and quotes from JSON files"  

    # Додаємо аргументи для командного рядка
    def add_arguments(self, parser):
        # Шляхи до файлів authors.json та quotes.json
        parser.add_argument("--authors", type=str, default="data/authors.json")
        parser.add_argument("--quotes", type=str, default="data/quotes.json")

    # Основний метод, який виконується при запуску команди
    # args - позиційні аргументи, options - ключові аргументи
    def handle(self, *args, **options):
        authors_file = Path(options["authors"]) # шлях до файлу authors.json
        quotes_file = Path(options["quotes"]) # шлях до файлу quotes.json

        # Перевіряємо, чи існують файли
        if not authors_file.exists() or not quotes_file.exists():
            self.stderr.write(  
                "JSON files not found. Provide correct --authors/--quotes paths."
            )
            return

        # Читаємо дані з JSON файлів
        with authors_file.open(encoding="utf-8") as f:
            authors = json.load(f)

        with quotes_file.open(encoding="utf-8") as f:
            quotes = json.load(f)

        # authors.json: [{ "fullname": ..., "born_date": ..., "born_location": ..., "description": ... }, ...]
        name2author = {}
        for a in authors:
            author, _ = Author.objects.get_or_create(
                fullname=a.get("fullname", "").strip(),
                defaults={
                    "born_date": a.get("born_date", ""),
                    "born_location": a.get("born_location", ""),
                    "description": a.get("description", ""),
                },
            )
            name2author[author.fullname] = author

        # quotes.json: [{ "quote": "...", "author": "Name", "tags": ["tag1","tag2"] }, ...]
        for q in quotes:
            text = q.get("quote", "").strip()
            author_name = q.get("author", "").strip()
            tags_list = q.get("tags", [])
            if not text or not author_name:
                continue
            author = name2author.get(author_name)
            if not author:
                # якщо автора не було в authors.json, створимо
                author, _ = Author.objects.get_or_create(fullname=author_name)
                name2author[author_name] = author  # зберігаємо автора для подальшого використання
            quote = Quote.objects.create(text=text, author=author) # створюємо цитату
            
            # обробляємо теги
            tag_objs = []
            for t in tags_list:
                t = t.strip() # видаляємо пробіли на початку та в кінці
                if not t:  
                    continue
                tag, _ = Tag.objects.get_or_create(name=t) 
                tag_objs.append(tag) # додаємо тег до списку
            if tag_objs: # якщо є теги, встановлюємо їх для цитати
                quote.tags.set(tag_objs)  
 
        # виводимо повідомлення про успішне завершення імпорту
        self.stdout.write(self.style.SUCCESS("Import finished"))
