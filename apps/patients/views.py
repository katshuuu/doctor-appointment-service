"""Страницы сущности «Пациент». Данные читаются из SQLite."""

from django.shortcuts import render

from db.database import fetch_all, fetch_one
from db.queries import (
    APPOINTMENTS_BY_PATIENT,
    MINOR_PATIENTS,
    PATIENT_BY_ID,
    PATIENTS,
)


def patients(request):
    """Список пациентов из таблицы patients."""
    context = {
        "patients": fetch_all(PATIENTS),
        "minors": fetch_all(MINOR_PATIENTS),
    }
    return render(request, "patients/patient_list.html", context)


def patient_detail(request, patient_id):
    """Карточка пациента и его записи."""
    patient = fetch_one(PATIENT_BY_ID, (patient_id,))
    if patient is None:
        return render(
            request,
            "patients/patient_detail.html",
            {"patient": None},
            status=404,
        )
    if patient["is_minor"]:
        minor_label = "несовершеннолетний"
    else:
        minor_label = "совершеннолетний"
    context = {
        "patient": patient,
        "appointments": fetch_all(
            APPOINTMENTS_BY_PATIENT,
            (patient_id,),
        ),
        "minor_label": minor_label,
    }
    return render(request, "patients/patient_detail.html", context)
