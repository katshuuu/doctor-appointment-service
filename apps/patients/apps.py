"""Конфигурация Django-приложения patients."""

from django.apps import AppConfig


class PatientsConfig(AppConfig):
    """Веб-страницы сущности «Пациент»."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.patients"
