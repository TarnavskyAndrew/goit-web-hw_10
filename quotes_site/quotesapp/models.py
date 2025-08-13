from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=150, unique=True)
    born_date = models.CharField(max_length=100, blank=True)
    born_location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.fullname


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    click_count = models.PositiveIntegerField(default=0)  # рахує кількість натискання на тег

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Quote(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="quotes")
    tags = models.ManyToManyField(Tag, related_name="quotes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.text[:60] + ("..." if len(self.text) > 60 else "")
