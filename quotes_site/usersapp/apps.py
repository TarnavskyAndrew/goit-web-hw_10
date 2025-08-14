from django.apps import AppConfig


# клас, який представляє додаток "usersapp"
class UsersappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField" # тип поля для первинного ключа
    name = "usersapp" # ім'я додатку

    # Метод, який викликається, коли додаток готовий
    def ready(self):
        import usersapp.signals  # імпортуємо, щоб сигнали працювали
