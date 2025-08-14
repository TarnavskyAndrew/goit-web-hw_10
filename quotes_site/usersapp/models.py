import os
import uuid
from django.utils.deconstruct import deconstructible
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Модель для зберігання профілю користувача з аватаром
# Використовуємо декоратор deconstructible для сумісності з міграціями
@deconstructible
class PathAndRename:
    def __init__(self, sub_path):  # приймаємо підшлях як аргумент
        self.path = sub_path # зберігаємо його як атрибут класу

    def __call__(self, instance, filename): # викликається при збереженні файлу
        ext = filename.split(".")[-1] # отримуємо розширення файлу
        # генеруємо унікальне ім'я
        filename = f"{uuid.uuid4().hex}.{ext}"  
        return os.path.join(self.path, filename)

# Функція для завантаження аватара користувача
def upload_to_avatar(instance, filename):
    ext = filename.split(".")[-1] # отримуємо розширення файлу
    filename = f"{uuid.uuid4().hex}.{ext}" # генеруємо унікальне ім'я
    return f"avatars/{filename}"  # шлях до аватара


# Модель профілю користувача з аватаром
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # зв'язок з користувачем
    avatar = models.ImageField(  # поле для аватара
        upload_to=upload_to_avatar, # функція для завантаження
        blank=True,     # дозволяємо порожнє поле
        null=True,     # дозволяємо null
        default="avatars/default_avatar.jpg",  # дефолтне фото
    )

    def __str__(self):
        return f"Profile of {self.user.username}"

    # Збереження аватара з обмеженням розміру
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # викликаємо базовий метод save

        if self.avatar: 
            img = Image.open(self.avatar.path)  # відкриваємо аватар
            max_size = (300, 300) # максимальний розмір

            try:
                resample_filter = Image.Resampling.LANCZOS # фільтр для ресемплінгу
            except AttributeError:
                resample_filter = Image.ANTIALIAS # для старих версій PIL

            img.thumbnail(max_size, resample_filter) # змінюємо розмір зображення
            img.save(self.avatar.path) # зберігаємо його
