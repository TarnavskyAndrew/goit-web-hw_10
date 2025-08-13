import json
from pathlib import Path
from django.core.management.base import BaseCommand
from quotesapp.models import Author, Tag, Quote


class Command(BaseCommand):
    help = "Load authors and quotes from JSON files"

    def add_arguments(self, parser):
        parser.add_argument("--authors", type=str, default="data/authors.json")
        parser.add_argument("--quotes", type=str, default="data/quotes.json")

    def handle(self, *args, **options):
        authors_file = Path(options["authors"])
        quotes_file = Path(options["quotes"])

        if not authors_file.exists() or not quotes_file.exists():
            self.stderr.write(
                "JSON files not found. Provide correct --authors/--quotes paths."
            )
            return

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
                name2author[author_name] = author
            quote = Quote.objects.create(text=text, author=author)

            tag_objs = []
            for t in tags_list:
                t = t.strip()
                if not t:
                    continue
                tag, _ = Tag.objects.get_or_create(name=t)
                tag_objs.append(tag)
            if tag_objs:
                quote.tags.set(tag_objs)

        self.stdout.write(self.style.SUCCESS("Import finished"))
