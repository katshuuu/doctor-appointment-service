#!/usr/bin/env python
"""Точка запуска административных команд Django."""
import os
import sys


def main():
    """Запустить команду Django из командной строки."""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "appointment_service.settings",
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Установите зависимости "
            "из requirements.txt и активируйте виртуальное окружение."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
