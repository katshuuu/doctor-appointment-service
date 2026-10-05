"""Страницы сущности «Врач»."""

from html import escape

from django.http import HttpResponse

from appointments import is_slot_available
from apps.homepage.views import page
from apps.loaders import load_domain, specialty_path
from doctors import find_doctor_by_id


def _not_found():
    content = """
    <h1 class="text-danger">Врач не найден</h1>
    <a href="/doctors/" class="btn btn-outline-secondary">
        ← к списку врачей
    </a>
    """
    return HttpResponse(
        page("Врач не найден", content),
        status=404,
    )


def doctors(request):
    """Список врачей из data/doctors.json."""
    doctor_list, _appointments = load_domain()
    items = ""
    for doctor in doctor_list:
        text = (
            f"{escape(doctor.name)} — {escape(doctor.specialty)}"
        )
        items += (
            '<li class="list-group-item">'
            f'<a href="/doctors/{doctor.id}/">{text}</a>'
            "</li>"
        )
    content = f"""
    <h1>Врачи</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Сервис записи к врачу – врачи", content))


def doctor_detail(request, doctor_id):
    """Карточка врача и проверка слота по логике ПР3."""
    doctor_list, appointments = load_domain()
    doctor = find_doctor_by_id(doctor_list, doctor_id)
    if doctor is None:
        return _not_found()

    own = [
        item for item in appointments
        if item.doctor.id == doctor.id
    ]
    active_count = sum(1 for item in own if not item.is_cancelled)
    slot_text = "Записей пока нет"
    badge = "bg-secondary"
    if own:
        sample = own[0]
        free = is_slot_available(
            appointments,
            doctor,
            sample.appointment_date,
            sample.appointment_time,
        )
        state = "свободен" if free else "занят"
        badge = "bg-success" if free else "bg-danger"
        slot_text = (
            f"{sample.appointment_date} "
            f"{sample.appointment_time}: {state}"
        )
    rows = ""
    for item in own:
        status = "отменена" if item.is_cancelled else "активна"
        status_badge = (
            "bg-secondary" if item.is_cancelled else "bg-success"
        )
        rows += (
            '<li class="list-group-item d-flex '
            'justify-content-between">'
            f'<a href="/appointments/{item.id}/">'
            f"{escape(item.patient.name)}</a>"
            f'<span class="badge {status_badge}">{status}</span>'
            "</li>"
        )
    specialty_link = specialty_path(doctor.specialty)
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{escape(doctor.name)}</h5>
            <p class="card-text"><strong>ID:</strong> {doctor.id}</p>
            <p class="card-text">
                <strong>Специальность:</strong>
                <a href="{specialty_link}">
                    {escape(doctor.specialty)}
                </a>
            </p>
            <p class="card-text">
                Активных записей: {active_count}
            </p>
            <p class="card-text">
                Слот первой записи:
                <span class="badge {badge}">{escape(slot_text)}</span>
            </p>
            <p class="card-text">Пациенты этого врача:</p>
            <ul class="list-group mb-3">{rows}</ul>
            <a href="/doctors/" class="btn btn-outline-secondary">
                ← к списку врачей
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(doctor.name, content), status=200)
