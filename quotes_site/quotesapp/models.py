from django.db import models


# клас для зберігання інформації про авторів цитат, теги та самі цитати
class Author(models.Model):
    fullname = models.CharField(max_length=150, unique=True) # повне ім'я автора, унікальне
    born_date = models.CharField(max_length=100, blank=True) # дата народження, може бути порожнім
    born_location = models.CharField(max_length=200, blank=True) # місце народження, може бути порожнім
    description = models.TextField(blank=True) # опис автора, може бути порожнім

    def __str__(self):
        return self.fullname


# клас для зберігання тегів цитат
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True) # назва тега, унікальна
    click_count = models.PositiveIntegerField(default=0)  # рахує кількість натискання на тег

    # клас мета для сортування тегів за назвою
    class Meta:
        ordering = ["name"]   

    def __str__(self):
        return self.name


# клас для зберігання цитат
class Quote(models.Model):
    text = models.TextField() # текст цитати
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="quotes") # зв'язок з автором, при видаленні автора видаляються і його цитати
    tags = models.ManyToManyField(Tag, related_name="quotes") # зв'язок з тегами, багато до багатьох
    created_at = models.DateTimeField(auto_now_add=True) # дата створення цитати, автоматично заповнюється при створенні
    
    # клас мета для сортування цитат за датою створення
    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.text[:60] + ("..." if len(self.text) > 60 else "")
