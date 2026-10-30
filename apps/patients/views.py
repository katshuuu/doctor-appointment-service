"""Страницы сущности «Пациент». Данные читаются через Django ORM."""

from django.shortcuts import render

from apps.appointments.models import Appointment
from apps.patients.models import MINOR_AGE_LIMIT, Patient


def patients(request):
    """Список пациентов и отдельно несовершеннолетние."""
    context = {
        "patients": Patient.objects.order_by("pk"),
        "minors": Patient.objects.filter(
            age__lt=MINOR_AGE_LIMIT,
        ).order_by("age"),
    }
    return render(request, "patients/patient_list.html", context)


def patient_detail(request, patient_id):
    """Карточка пациента и его записи."""
    try:
        patient = Patient.objects.get(pk=patient_id)
    except Patient.DoesNotExist:
        return render(
            request,
            "patients/patient_detail.html",
            {"patient": None},
            status=404,
        )
    if patient.is_minor:
        minor_label = "несовершеннолетний"
    else:
        minor_label = "совершеннолетний"
    appointments = Appointment.objects.filter(
        patient_id=patient.pk,
    ).select_related(
        "doctor",
        "doctor__specialty",
    ).order_by("appointment_date", "appointment_time")
    context = {
        "patient": patient,
        "appointments": appointments,
        "minor_label": minor_label,
    }
    return render(request, "patients/patient_detail.html", context)
