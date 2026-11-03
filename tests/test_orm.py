"""Проверка моделей Django ORM: связи, создание, изменение, удаление."""

from datetime import date, time

import pytest
from django.db import transaction
from django.db.models.deletion import ProtectedError

from apps.appointments.models import Appointment
from apps.doctors.models import Doctor
from apps.patients.models import Patient
from apps.specialties.models import Specialty


def test_related_objects_and_crud_do_not_change_source_rows():
    """Связи читаются, а пробные записи откатываются."""
    doctor = Doctor.objects.select_related("specialty").get(pk=1)
    appointment = Appointment.objects.select_related(
        "doctor",
        "patient",
    ).get(pk=1)
    assert doctor.specialty.name == "Терапевт"
    assert appointment.patient.name == "Иванов Иван Иванович"
    assert appointment.doctor.appointments.filter(pk=1).exists()
    assert doctor.specialty.doctors.filter(pk=1).exists()

    with transaction.atomic():
        specialty = Specialty.objects.create(name="Проверочная специальность")
        new_doctor = Doctor.objects.create(
            name="Проверочный врач",
            specialty=specialty,
        )
        new_patient = Patient.objects.create(
            name="Проверочный пациент",
            age=40,
        )
        new_appointment = Appointment.objects.create(
            doctor=new_doctor,
            patient=new_patient,
            appointment_date=date(2026, 1, 2),
            appointment_time=time(9, 0),
        )
        new_appointment.cancel()
        new_appointment.refresh_from_db()
        assert new_appointment.status == Appointment.Status.CANCELLED
        with pytest.raises(ProtectedError):
            new_doctor.delete()
        new_appointment.delete()
        new_doctor.delete()
        new_patient.delete()
        specialty.delete()
        transaction.set_rollback(True)

    assert Doctor.objects.filter(name="Проверочный врач").count() == 0
    assert Appointment.objects.cancelled().count() == 3
