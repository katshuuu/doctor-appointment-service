"""Главная страница и обработчик неизвестного адреса."""

from django.shortcuts import render

from apps.loaders import load_domain


def index(request):
    """Главная страница: описание сервиса и переход к разделам."""
    doctors, appointments = load_domain()
    context = {
        "doctors": doctors,
        "appointments": appointments,
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request, exception):
    """Собственная страница для адреса, которому нет маршрута."""
    return render(
        request,
        "404.html",
        status=404,
    )
