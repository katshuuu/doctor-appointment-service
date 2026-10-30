"""Страницы сущности «Врач». Данные читаются через Django ORM."""

from datetime import datetime

from django.shortcuts import render

from apps.appointments.models import Appointment
from apps.doctors.models import Doctor


def doctors(request):
    """Список врачей. Пустое имя показывает всех, иначе поиск по имени."""
    search_name = request.GET.get("name", "").strip()
    doctor_list = Doctor.objects.select_related("specialty")
    if search_name:
        doctor_list = doctor_list.filter(
            name__icontains=search_name,
        ).order_by("name")
    else:
        doctor_list = doctor_list.order_by("pk")
    context = {
        "doctors": doctor_list,
        "search_name": search_name,
    }
    return render(request, "doctors/doctor_list.html", context)


def available_doctors(request):
    """Врачи без активной записи на выбранную дату."""
    appointment_date = request.GET.get("date", "").strip()
    doctor_list = []
    error = None
    if appointment_date:
        try:
            selected_date = datetime.strptime(
                appointment_date,
                "%Y-%m-%d",
            ).date()
        except ValueError:
            error = "Укажите корректную дату."
        else:
            booked_ids = Appointment.objects.filter(
                appointment_date=selected_date,
                is_cancelled=False,
            ).values_list("doctor_id", flat=True)
            doctor_list = Doctor.objects.exclude(
                pk__in=booked_ids,
            ).select_related("specialty").order_by("name")
    context = {
        "doctors": doctor_list,
        "appointment_date": appointment_date,
        "error": error,
    }
    return render(request, "doctors/available.html", context)


def doctor_detail(request, doctor_id):
    """Карточка врача. Занятость слота считается по активным записям."""
    try:
        doctor = Doctor.objects.select_related("specialty").get(
            pk=doctor_id,
        )
    except Doctor.DoesNotExist:
        return render(
            request,
            "doctors/doctor_detail.html",
            {"doctor": None},
            status=404,
        )
    own = Appointment.objects.filter(
        doctor_id=doctor.pk,
    ).select_related("patient").order_by("pk")
    active_count = own.filter(is_cancelled=False).count()
    slot_text = "Записей пока нет"
    slot_badge = "bg-secondary"
    sample = own.first()
    if sample is not None:
        busy = own.filter(
            is_cancelled=False,
            appointment_date=sample.appointment_date,
            appointment_time=sample.appointment_time,
        ).exists()
        state = "занят" if busy else "свободен"
        slot_badge = "bg-danger" if busy else "bg-success"
        slot_text = (
            f"{sample.appointment_date.isoformat()} "
            f"{sample.appointment_time.strftime('%H:%M:%S')}: {state}"
        )
    context = {
        "doctor": doctor,
        "appointments": own,
        "active_count": active_count,
        "slot_text": slot_text,
        "slot_badge": slot_badge,
    }
    return render(request, "doctors/doctor_detail.html", context)
