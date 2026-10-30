"""Главная страница и обработчик неизвестного адреса."""

from django.shortcuts import render

from apps.appointments.models import Appointment
from apps.doctors.models import Doctor


def index(request):
    """Главная страница: описание сервиса и переход к разделам."""
    context = {
        "doctors": Doctor.objects.order_by("pk"),
        "appointments": Appointment.objects.order_by("pk"),
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request, exception):
    """Собственная страница для адреса, которому нет маршрута."""
    return render(
        request,
        "404.html",
        status=404,
    )
