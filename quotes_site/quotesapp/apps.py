from django.apps import AppConfig

#клас для конфігурації додатку quotesapp
class QuotesappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField" # Тип поля для первинного ключа
    name = "quotesapp" # Ім'я додатку, яке буде використовуватися в Django
