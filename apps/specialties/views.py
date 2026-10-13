"""Страницы сущности «Специальность». Данные читаются из SQLite."""

from django.shortcuts import render

from db.database import fetch_all, fetch_one
from db.queries import (
    DOCTORS_BY_SPECIALTY,
    DOCTORS_OF_SPECIALTY,
    SPECIALTY_BY_NAME,
)


def specialties(request):
    """Справочник специальностей и число врачей по каждой."""
    context = {
        "specialties": fetch_all(DOCTORS_BY_SPECIALTY),
    }
    return render(
        request,
        "specialties/specialty_list.html",
        context,
    )


def specialty_detail(request, specialty_name):
    """Врачи выбранной специальности."""
    specialty = fetch_one(SPECIALTY_BY_NAME, (specialty_name,))
    if specialty is None:
        return render(
            request,
            "specialties/specialty_detail.html",
            {"specialty": None},
            status=404,
        )
    doctors = fetch_all(DOCTORS_OF_SPECIALTY, (specialty_name,))
    context = {
        "specialty": specialty["name"],
        "doctors": doctors,
    }
    return render(
        request,
        "specialties/specialty_detail.html",
        context,
    )
