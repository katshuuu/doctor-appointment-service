"""Страницы сущности «Врач». Данные читаются из SQLite."""

from django.shortcuts import render

from db.database import fetch_all, fetch_one
from db.queries import (
    APPOINTMENTS_BY_DOCTOR,
    DOCTOR_BY_ID,
    DOCTORS,
    DOCTORS_BY_NAME,
    FREE_DOCTORS,
)


def doctors(request):
    """Список врачей. Пустое имя показывает всех, иначе срабатывает LIKE."""
    search_name = request.GET.get("name", "").strip()
    if search_name:
        doctor_list = fetch_all(DOCTORS_BY_NAME, (search_name,))
    else:
        doctor_list = fetch_all(DOCTORS)
    context = {
        "doctors": doctor_list,
        "search_name": search_name,
    }
    return render(request, "doctors/doctor_list.html", context)


def available_doctors(request):
    """Врачи без активной записи на выбранную дату."""
    appointment_date = request.GET.get("date", "").strip()
    doctor_list = []
    if appointment_date:
        doctor_list = fetch_all(FREE_DOCTORS, (appointment_date,))
    context = {
        "doctors": doctor_list,
        "appointment_date": appointment_date,
    }
    return render(request, "doctors/available.html", context)


def doctor_detail(request, doctor_id):
    """Карточка врача. Занятость слота считается по активным записям."""
    doctor = fetch_one(DOCTOR_BY_ID, (doctor_id,))
    if doctor is None:
        return render(
            request,
            "doctors/doctor_detail.html",
            {"doctor": None},
            status=404,
        )
    own = fetch_all(APPOINTMENTS_BY_DOCTOR, (doctor_id,))
    active_count = sum(1 for item in own if not item["is_cancelled"])
    slot_text = "Записей пока нет"
    slot_badge = "bg-secondary"
    if own:
        sample = own[0]
        busy = any(
            not item["is_cancelled"]
            and item["appointment_date"] == sample["appointment_date"]
            and item["appointment_time"] == sample["appointment_time"]
            for item in own
        )
        state = "занят" if busy else "свободен"
        slot_badge = "bg-danger" if busy else "bg-success"
        slot_text = (
            f"{sample['appointment_date']} "
            f"{sample['appointment_time']}: {state}"
        )
    context = {
        "doctor": doctor,
        "appointments": own,
        "active_count": active_count,
        "slot_text": slot_text,
        "slot_badge": slot_badge,
    }
    return render(request, "doctors/doctor_detail.html", context)
