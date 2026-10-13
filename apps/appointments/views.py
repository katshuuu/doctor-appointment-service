"""Страницы сущности «Запись на прием». Данные читаются из SQLite."""

from django.shortcuts import render

from db.database import fetch_all, fetch_one
from db.queries import (
    ACTIVE_APPOINTMENTS_COUNT,
    APPOINTMENT_BY_ID,
    APPOINTMENTS,
    BUSY_DOCTORS,
    PATIENT_AGE_STATS,
    STATS_BY_DOCTOR,
)


def appointments(request):
    """Список записей со связанными врачом и пациентом."""
    context = {
        "appointments": fetch_all(APPOINTMENTS),
        "active_count": fetch_one(ACTIVE_APPOINTMENTS_COUNT),
    }
    return render(
        request,
        "appointments/appointment_list.html",
        context,
    )


def appointment_detail(request, appointment_id):
    """Карточка записи со связанными врачом и пациентом."""
    appointment = fetch_one(APPOINTMENT_BY_ID, (appointment_id,))
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


def statistics(request):
    """Число активных записей по врачам и сводка по возрасту."""
    context = {
        "statistics": fetch_all(STATS_BY_DOCTOR),
        "busy_doctors": fetch_all(BUSY_DOCTORS),
        "active_count": fetch_one(ACTIVE_APPOINTMENTS_COUNT),
        "ages": fetch_one(PATIENT_AGE_STATS),
    }
    return render(
        request,
        "appointments/statistics.html",
        context,
    )
