"""Страницы сущности «Запись на прием»."""

from django.shortcuts import render

from appointments import find_appointment_by_id
from apps.loaders import load_domain


def appointments(request):
    """Список записей из data/appointments.json."""
    _doctors, appointment_list = load_domain()
    context = {
        "appointments": appointment_list,
    }
    return render(
        request,
        "appointments/appointment_list.html",
        context,
    )


def appointment_detail(request, appointment_id):
    """Карточка записи со связанными врачом и пациентом."""
    _doctors, appointment_list = load_domain()
    appointment = find_appointment_by_id(
        appointment_list,
        appointment_id,
    )
    if appointment is None:
        return render(
            request,
            "appointments/appointment_detail.html",
            {"appointment": None},
            status=404,
        )
    context = {
        "appointment": appointment,
    }
    return render(
        request,
        "appointments/appointment_detail.html",
        context,
    )
