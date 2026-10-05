"""Конфигурация Django-приложения appointments."""

from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    """Веб-страницы сущности «Запись на прием»."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.appointments"
