"""Страницы сущности «Пациент»."""

from django.shortcuts import render

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
    context = {
        "patients": unique_patients(appointments),
    }
    return render(request, "patients/patient_list.html", context)


def patient_detail(request, patient_id):
    """Карточка пациента и его записи."""
    _doctors, appointments = load_domain()
    patients_list = unique_patients(appointments)
    if patient_id < 1 or patient_id > len(patients_list):
        return render(
            request,
            "patients/patient_detail.html",
            {"patient": None},
            status=404,
        )
    patient = patients_list[patient_id - 1]
    if patient.is_minor():
        minor_label = "несовершеннолетний"
    else:
        minor_label = "совершеннолетний"
    context = {
        "patient": patient,
        "appointments": _patient_appointments(
            patient,
            appointments,
        ),
        "minor_label": minor_label,
    }
    return render(
        request,
        "patients/patient_detail.html",
        context,
    )
