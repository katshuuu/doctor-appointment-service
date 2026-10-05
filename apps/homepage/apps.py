"""Конфигурация Django-приложения homepage."""

from django.apps import AppConfig


class HomepageConfig(AppConfig):
    """Главная страница сервиса записи к врачу."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.homepage"
