"""Страницы сущности «Запись на прием»."""

from html import escape

from django.http import HttpResponse

from appointments import find_appointment_by_id
from apps.homepage.views import page
from apps.loaders import load_domain, specialty_path


def appointments(request):
    """Список записей из data/appointments.json."""
    _doctors, appointment_list = load_domain()
    items = ""
    for appointment in appointment_list:
        status = "отменена" if appointment.is_cancelled else "активна"
        badge = (
            "bg-secondary" if appointment.is_cancelled else "bg-success"
        )
        label = (
            f"{escape(appointment.patient.name)} → "
            f"{escape(appointment.doctor.name)}, "
            f"{appointment.appointment_date}"
        )
        items += (
            '<li class="list-group-item d-flex '
            'justify-content-between">'
            f'<a href="/appointments/{appointment.id}/">{label}</a>'
            f'<span class="badge {badge}">{status}</span>'
            "</li>"
        )
    content = f"""
    <h1>Записи на прием</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(
        page("Сервис записи к врачу – записи", content),
    )


def appointment_detail(request, appointment_id):
    """Карточка записи со связанными врачом и пациентом."""
    _doctors, appointment_list = load_domain()
    appointment = find_appointment_by_id(
        appointment_list,
        appointment_id,
    )
    if appointment is None:
        content = """
        <h1 class="text-danger">Запись не найдена</h1>
        <a href="/appointments/" class="btn btn-outline-secondary">
            ← к списку записей
        </a>
        """
        return HttpResponse(
            page("Запись не найдена", content),
            status=404,
        )
    status = "отменена" if appointment.is_cancelled else "активна"
    badge = "bg-secondary" if appointment.is_cancelled else "bg-success"
    minor = (
        "да" if appointment.patient.is_minor() else "нет"
    )
    specialty_link = specialty_path(appointment.doctor.specialty)
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Запись №{appointment.id}</h5>
            <p class="card-text">
                Пациент:
                {escape(appointment.patient.name)},
                возраст {appointment.patient.age}
            </p>
            <p class="card-text">
                Несовершеннолетний: {minor}
            </p>
            <p class="card-text">
                Врач:
                <a href="/doctors/{appointment.doctor.id}/">
                    {escape(appointment.doctor.name)}
                </a>
            </p>
            <p class="card-text">
                Специальность:
                <a href="{specialty_link}">
                    {escape(appointment.doctor.specialty)}
                </a>
            </p>
            <p class="card-text">
                Дата: {appointment.appointment_date}
            </p>
            <p class="card-text">
                Время: {appointment.appointment_time}
            </p>
            <p class="card-text">
                Статус:
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/appointments/" class="btn btn-outline-secondary">
                ← к списку записей
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Запись №{appointment.id}", content),
        status=200,
    )
