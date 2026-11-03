"""Общие данные сервиса для шаблонов."""

from .models import Doctor


def site_context(request):
    """Передать название сервиса и число врачей во все шаблоны."""
    return {
        "site_name": "Сервис записи к врачу",
        "doctors_count": Doctor.objects.count(),
    }
