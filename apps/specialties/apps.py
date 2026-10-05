"""Конфигурация Django-приложения specialties."""

from django.apps import AppConfig


class SpecialtiesConfig(AppConfig):
    """Веб-страницы сущности «Специальность»."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.specialties"
