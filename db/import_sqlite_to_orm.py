"""Перенос данных из базы ПР7 в таблицы Django ORM.

Исходный файл data/doctor_appointment.sqlite не изменяется.
Django пишет в базу из DATABASES, обычно db.sqlite3.
Запуск после migrate: python db/import_sqlite_to_orm.py
"""

import os
import sqlite3
import sys
from datetime import date, time
from pathlib import Path

import django
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DB = BASE_DIR / "data" / "doctor_appointment.sqlite"

sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "appointment_service.settings",
)
django.setup()

from apps.appointments.models import Appointment  # noqa: E402
from apps.doctors.models import Doctor  # noqa: E402
from apps.patients.models import Patient  # noqa: E402
from apps.specialties.models import Specialty  # noqa: E402


def main():
    """Перенести специальности, врачей, пациентов и записи."""
    if not SOURCE_DB.exists():
        raise FileNotFoundError(
            f"Исходная база не найдена: {SOURCE_DB}"
        )
    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row
        specialties = connection.execute(
            """
            SELECT id, name
            FROM specialties
            ORDER BY id
            """
        ).fetchall()
        doctors = connection.execute(
            """
            SELECT id, name, specialty_id
            FROM doctors
            ORDER BY id
            """
        ).fetchall()
        patients = connection.execute(
            """
            SELECT id, name, age
            FROM patients
            ORDER BY id
            """
        ).fetchall()
        appointments = connection.execute(
            """
            SELECT
                id,
                doctor_id,
                patient_id,
                appointment_date,
                appointment_time,
                is_cancelled
            FROM appointments
            ORDER BY id
            """
        ).fetchall()
        with transaction.atomic():
            for row in specialties:
                Specialty.objects.update_or_create(
                    pk=row["id"],
                    defaults={"name": row["name"]},
                )
            for row in doctors:
                Doctor.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                        "specialty_id": row["specialty_id"],
                    },
                )
            for row in patients:
                Patient.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                        "age": row["age"],
                    },
                )
            for row in appointments:
                Appointment.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "doctor_id": row["doctor_id"],
                        "patient_id": row["patient_id"],
                        "appointment_date": date.fromisoformat(
                            row["appointment_date"]
                        ),
                        "appointment_time": time.fromisoformat(
                            row["appointment_time"]
                        ),
                        "is_cancelled": bool(row["is_cancelled"]),
                    },
                )
    print("Перенос данных завершён.")
    print(f"Специальностей: {Specialty.objects.count()}")
    print(f"Врачей: {Doctor.objects.count()}")
    print(f"Пациентов: {Patient.objects.count()}")
    print(f"Записей: {Appointment.objects.count()}")


if __name__ == "__main__":
    main()
