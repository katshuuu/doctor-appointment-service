"""Перед веб-тестами переносит данные ПР7 в базу Django."""

import os

import django
import pytest

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "appointment_service.settings",
)
django.setup()


@pytest.fixture(scope="session", autouse=True)
def load_orm_data():
    """Применить миграции и заполнить базу из исходного SQLite."""
    from django.core.management import call_command

    call_command("migrate", verbosity=0, interactive=False)
    from db.import_sqlite_to_orm import main
    main()
