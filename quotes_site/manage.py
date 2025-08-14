#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


# Цей файл є точкою входу для виконання команд Django з командного рядка.
def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line # імпортуємо функцію для виконання команд з командного рядка
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv) # робить виклик команди, яку передали в sys.argv


if __name__ == "__main__":
    main()
