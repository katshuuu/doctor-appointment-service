"""Страницы сущности «Запись на прием». Данные читаются через ORM."""

from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Max, Min, Q
from django.shortcuts import render

from apps.appointments.models import Appointment
from apps.doctors.models import Doctor
from apps.patients.models import Patient

SORT_FIELDS = {
    "date": ("appointment_date", "appointment_time", "pk"),
    "doctor": ("doctor__name", "appointment_date", "pk"),
    "patient": ("patient__name", "appointment_date", "pk"),
}
PAGE_SIZE = 5


def _parse_date(raw_value):
    """Вернуть дату или None, если строка не в формате YYYY-MM-DD."""
    try:
        return datetime.strptime(raw_value, "%Y-%m-%d").date()
    except ValueError:
        return None


def appointments(request):
    """Список записей: фильтры, поиск, сортировка и страницы."""
    appointment_date = request.GET.get("date", "").strip()
    doctor_id = request.GET.get("doctor", "").strip()
    patient_id = request.GET.get("patient", "").strip()
    search_text = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    sort = request.GET.get("sort", "date")
    error = None

    rows = Appointment.objects.select_related(
        "doctor",
        "doctor__specialty",
        "patient",
    ).annotate(
        doctor_name=F("doctor__name"),
        patient_name=F("patient__name"),
    )
    if appointment_date:
        selected_date = _parse_date(appointment_date)
        if selected_date is None:
            error = "Укажите корректную дату."
        else:
            rows = rows.for_date(selected_date)
    if doctor_id.isdigit():
        rows = rows.filter(doctor_id=int(doctor_id))
    if patient_id.isdigit():
        rows = rows.filter(patient_id=int(patient_id))
    if status == Appointment.Status.ACTIVE:
        rows = rows.active()
    elif status == Appointment.Status.CANCELLED:
        rows = rows.cancelled()
    elif status == Appointment.Status.COMPLETED:
        rows = rows.completed()
    if search_text:
        rows = rows.filter(
            Q(patient__name__icontains=search_text)
            | Q(doctor__name__icontains=search_text)
        )
    if sort not in SORT_FIELDS:
        sort = "date"
    rows = rows.order_by(*SORT_FIELDS[sort])

    paginator = Paginator(rows, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))
    status_counts = Appointment.objects.aggregate(
        appointments_count=Count(
            "pk",
            filter=Q(status=Appointment.Status.ACTIVE),
        ),
        cancelled_count=Count(
            "pk",
            filter=Q(status=Appointment.Status.CANCELLED),
        ),
        completed_count=Count(
            "pk",
            filter=Q(status=Appointment.Status.COMPLETED),
        ),
    )
    context = {
        "appointments": page_obj,
        "page_obj": page_obj,
        "active_count": status_counts,
        "appointment_date": appointment_date,
        "selected_doctor": doctor_id,
        "selected_patient": patient_id,
        "search_text": search_text,
        "selected_status": status,
        "status_choices": Appointment.Status.choices,
        "sort": sort,
        "error": error,
        "doctors": Doctor.objects.order_by("name"),
        "patients": Patient.objects.order_by("name"),
    }
    return render(
        request,
        "appointments/appointment_list.html",
        context,
    )


def appointment_detail(request, appointment_id):
    """Карточка записи со связанными врачом и пациентом."""
    try:
        appointment = Appointment.objects.select_related(
            "doctor",
            "doctor__specialty",
            "patient",
        ).get(pk=appointment_id)
    except Appointment.DoesNotExist:
        return render(
            request,
            "appointments/appointment_detail.html",
            {"appointment": None},
            status=404,
        )
    return render(
        request,
        "appointments/appointment_detail.html",
        {"appointment": appointment},
    )


def statistics(request):
    """Число записей по статусам, по врачам и сводка по возрасту."""
    def count_by_status(status):
        return Count(
            "appointments",
            filter=Q(appointments__status=status),
        )

    statistics_data = Doctor.objects.annotate(
        appointments_count=count_by_status(Appointment.Status.ACTIVE),
        doctor_name=F("name"),
    ).values(
        "doctor_name",
        "appointments_count",
    ).order_by("-appointments_count", "name")
    busy_doctors = Doctor.objects.annotate(
        appointments_count=count_by_status(Appointment.Status.ACTIVE),
        doctor_name=F("name"),
    ).filter(
        appointments_count__gt=1,
    ).values(
        "doctor_name",
        "appointments_count",
    ).order_by("-appointments_count", "name")
    status_counts = Appointment.objects.aggregate(
        total_bookings=Count("pk"),
        appointments_count=Count(
            "pk",
            filter=Q(status=Appointment.Status.ACTIVE),
        ),
        cancelled_bookings=Count(
            "pk",
            filter=Q(status=Appointment.Status.CANCELLED),
        ),
        completed_bookings=Count(
            "pk",
            filter=Q(status=Appointment.Status.COMPLETED),
        ),
    )
    ages = Patient.objects.aggregate(
        patients_count=Count("pk"),
        average_age=Avg("age"),
        min_age=Min("age"),
        max_age=Max("age"),
    )
    context = {
        "statistics": statistics_data,
        "busy_doctors": busy_doctors,
        "active_count": status_counts,
        "ages": ages,
    }
    return render(
        request,
        "appointments/statistics.html",
        context,
    )
