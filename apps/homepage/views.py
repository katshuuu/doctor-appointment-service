"""Главная страница и обработчик неизвестного адреса."""

from django.shortcuts import render

from db.database import fetch_all, fetch_one
from db.queries import ACTIVE_APPOINTMENTS_COUNT, APPOINTMENTS, DOCTORS


def index(request):
    """Главная страница: описание сервиса и переход к разделам."""
    context = {
        "doctors": fetch_all(DOCTORS),
        "appointments": fetch_all(APPOINTMENTS),
        "active_count": fetch_one(ACTIVE_APPOINTMENTS_COUNT),
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request, exception):
    """Собственная страница для адреса, которому нет маршрута."""
    return render(
        request,
        "404.html",
        status=404,
    )
