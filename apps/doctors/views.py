"""Страницы сущности «Врач»."""

from django.shortcuts import render

from appointments import is_slot_available
from apps.loaders import load_domain
from doctors import find_doctor_by_id


def doctors(request):
    """Список врачей из data/doctors.json."""
    doctor_list, _appointments = load_domain()
    context = {
        "doctors": doctor_list,
    }
    return render(request, "doctors/doctor_list.html", context)


def doctor_detail(request, doctor_id):
    """Карточка врача и проверка слота по логике ПР3."""
    doctor_list, appointments = load_domain()
    doctor = find_doctor_by_id(doctor_list, doctor_id)
    if doctor is None:
        return render(
            request,
            "doctors/doctor_detail.html",
            {"doctor": None},
            status=404,
        )

    own = [
        item for item in appointments
        if item.doctor.id == doctor.id
    ]
    active_count = sum(
        1 for item in own if not item.is_cancelled
    )
    slot_text = "Записей пока нет"
    slot_badge = "bg-secondary"
    if own:
        sample = own[0]
        free = is_slot_available(
            appointments,
            doctor,
            sample.appointment_date,
            sample.appointment_time,
        )
        state = "свободен" if free else "занят"
        slot_badge = "bg-success" if free else "bg-danger"
        slot_text = (
            f"{sample.appointment_date} "
            f"{sample.appointment_time}: {state}"
        )
    context = {
        "doctor": doctor,
        "appointments": own,
        "active_count": active_count,
        "slot_text": slot_text,
        "slot_badge": slot_badge,
    }
    return render(request, "doctors/doctor_detail.html", context)
