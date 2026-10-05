"""Конфигурация Django-приложения doctors."""

from django.apps import AppConfig


class DoctorsConfig(AppConfig):
    """Веб-страницы сущности «Врач»."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.doctors"
