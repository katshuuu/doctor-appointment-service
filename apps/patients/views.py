"""Страницы сущности «Пациент»."""

from html import escape

from django.http import HttpResponse

from apps.homepage.views import page
from apps.loaders import load_domain


def unique_patients(appointments):
    """Пациенты в порядке первого появления в записях."""
    patients = []
    seen = set()
    for appointment in appointments:
        patient = appointment.patient
        key = (patient.name, patient.age)
        if key in seen:
            continue
        seen.add(key)
        patients.append(patient)
    return patients


def _patient_appointments(patient, appointments):
    return [
        item for item in appointments
        if (
            item.patient.name == patient.name
            and item.patient.age == patient.age
        )
    ]


def patients(request):
    """Список пациентов, восстановленных из записей на прием."""
    _doctors, appointments = load_domain()
    items = ""
    found = unique_patients(appointments)
    for index, patient in enumerate(found, start=1):
        minor = (
            "несовершеннолетний" if patient.is_minor()
            else "совершеннолетний"
        )
        if patient.is_minor():
            badge = "bg-warning text-dark"
        else:
            badge = "bg-light text-dark"
        items += (
            '<li class="list-group-item d-flex '
            'justify-content-between">'
            f'<a href="/patients/{index}/">{escape(patient.name)}</a>'
            f'<span class="badge {badge}">{minor}</span>'
            "</li>"
        )
    content = f"""
    <h1>Пациенты</h1>
    <p>
        Отдельного файла пациентов нет: объект Patient хранится
        внутри записи на прием.
    </p>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(
        page("Сервис записи к врачу – пациенты", content),
    )


def patient_detail(request, patient_id):
    """Карточка пациента и его записи."""
    _doctors, appointments = load_domain()
    patients_list = unique_patients(appointments)
    if patient_id < 1 or patient_id > len(patients_list):
        content = """
        <h1 class="text-danger">Пациент не найден</h1>
        <a href="/patients/" class="btn btn-outline-secondary">
            ← к списку пациентов
        </a>
        """
        return HttpResponse(
            page("Пациент не найден", content),
            status=404,
        )
    patient = patients_list[patient_id - 1]
    minor = patient.is_minor()
    minor_text = (
        "несовершеннолетний" if minor else "совершеннолетний"
    )
    badge = "bg-warning text-dark" if minor else "bg-success"
    rows = ""
    for item in _patient_appointments(patient, appointments):
        status = "отменена" if item.is_cancelled else "активна"
        rows += (
            '<li class="list-group-item">'
            f'<a href="/appointments/{item.id}/">'
            f"{escape(item.doctor.name)}, "
            f"{item.appointment_date} {item.appointment_time}"
            f"</a> — {status}"
            "</li>"
        )
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{escape(patient.name)}</h5>
            <p class="card-text">
                <strong>Возраст:</strong> {patient.age}
            </p>
            <p class="card-text">
                Статус:
                <span class="badge {badge}">{minor_text}</span>
            </p>
            <p class="card-text">{escape(str(patient))}</p>
            <p class="card-text">Записи пациента:</p>
            <ul class="list-group mb-3">{rows}</ul>
            <a href="/patients/" class="btn btn-outline-secondary">
                ← к списку пациентов
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(patient.name, content), status=200)
