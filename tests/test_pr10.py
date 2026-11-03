"""Проверки ПР10: статусы, менеджер, slug и вычисляемые поля."""

from datetime import date, time

from django.db.models import Count, Q
from django.test import Client, override_settings
from django.urls import reverse

from apps.appointments.models import Appointment
from apps.doctors.models import Doctor, build_doctor_slug
from apps.patients.models import Patient
from apps.specialties.models import Specialty


def test_appointment_queryset_methods_split_statuses():
    """active, cancelled и completed возвращают разные наборы."""
    total = Appointment.objects.count()
    active = Appointment.objects.active().count()
    cancelled = Appointment.objects.cancelled().count()
    completed = Appointment.objects.completed().count()
    assert active + cancelled + completed == total
    assert cancelled == 3
    assert completed == 0
    assert Appointment.objects.for_date(date(2026, 9, 15)).count() == 3


def test_status_migration_maps_cancelled_records():
    """Отменённые записи ПР7 получили статус cancelled."""
    cancelled_ids = set(
        Appointment.objects.cancelled().values_list("pk", flat=True),
    )
    assert cancelled_ids == {3, 7, 12}
    assert Appointment.objects.get(pk=1).status == Appointment.Status.ACTIVE


def test_available_doctors_ignore_cancelled_and_completed():
    """Занятость врача считается только по активным записям."""
    selected_date = date(2026, 9, 15)
    booked_ids = list(
        Appointment.objects.active().for_date(selected_date).values_list(
            "doctor_id",
            flat=True,
        ),
    )
    client = Client(HTTP_HOST="localhost")
    page = client.get("/doctors/available/?date=2026-09-15").content.decode()
    assert Doctor.objects.get(pk=1).pk in booked_ids
    assert "Смирнова Анна Сергеевна" not in page
    assert "Петров Олег Викторович" in page


def test_completed_appointment_does_not_block_doctor():
    """Завершённая запись не исключает врача из свободных."""
    specialty = Specialty.objects.create(name="Проверка статуса")
    doctor = Doctor.objects.create(
        name="Завершённый слот",
        specialty=specialty,
    )
    patient = Patient.objects.create(name="Пациент проверки", age=33)
    Appointment.objects.create(
        doctor=doctor,
        patient=patient,
        appointment_date=date(2026, 9, 20),
        appointment_time=time(10, 0),
        status=Appointment.Status.COMPLETED,
    )
    booked_ids = Appointment.objects.active().for_date(
        date(2026, 9, 20),
    ).values_list("doctor_id", flat=True)
    assert doctor.pk not in booked_ids
    Appointment.objects.filter(doctor=doctor).delete()
    doctor.delete()
    patient.delete()
    specialty.delete()


def test_statistics_count_all_three_statuses():
    """Статистика считает ACTIVE, CANCELLED и COMPLETED."""
    stats = Appointment.objects.aggregate(
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
    assert stats["total_bookings"] == 15
    assert stats["appointments_count"] == 12
    assert stats["cancelled_bookings"] == 3
    assert stats["completed_bookings"] == 0
    client = Client(HTTP_HOST="localhost")
    page = client.get("/appointments/statistics/").content.decode()
    assert "Отменённых: 3" in page
    assert "Завершённых: 0" in page


def test_doctor_slug_and_absolute_url():
    """Подробная страница врача открывается по slug."""
    doctor = Doctor.objects.get(pk=1)
    expected_slug = build_doctor_slug(doctor.name, doctor.pk)
    assert doctor.slug == expected_slug
    assert doctor.get_absolute_url() == reverse(
        "doctors:detail",
        kwargs={"slug": doctor.slug},
    )
    client = Client(HTTP_HOST="localhost")
    response = client.get(doctor.get_absolute_url())
    assert response.status_code == 200
    assert doctor.name in response.content.decode()


def test_generated_is_minor_comes_from_database():
    """Признак несовершеннолетнего считает база данных."""
    adult = Patient.objects.create(name="Взрослый", age=20)
    minor = Patient.objects.create(name="Ребёнок", age=12)
    adult.refresh_from_db()
    minor.refresh_from_db()
    assert adult.is_minor is False
    assert minor.is_minor is True
    adult.age = 10
    adult.save(update_fields=["age"])
    adult.refresh_from_db()
    assert adult.is_minor is True
    adult.delete()
    minor.delete()


def test_context_processor_adds_site_data():
    """Контекстный процессор передаёт название и число врачей."""
    client = Client(HTTP_HOST="localhost")
    page = client.get("/").content.decode()
    assert "Врачи (15)" in page
    assert "Сервис записи к врачу" in page


@override_settings(DEBUG=True)
def test_debug_toolbar_is_connected_in_debug():
    """При DEBUG панель отладки подключена к проекту."""
    from django.conf import settings

    assert "debug_toolbar" in settings.INSTALLED_APPS
