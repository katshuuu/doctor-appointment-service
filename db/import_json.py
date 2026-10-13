"""Перенос данных из JSON-файлов в таблицы SQLite."""

import json
from pathlib import Path

from db.database import apply_schema, get_connection
from entities.specialty import KNOWN_SPECIALTIES

BASE_DIR = Path(__file__).resolve().parent.parent
DOCTORS_FILE = BASE_DIR / "data" / "doctors.json"
APPOINTMENTS_FILE = BASE_DIR / "data" / "appointments.json"


def load_json(path):
    """Прочитать JSON-файл проекта."""
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def clear_tables(conn):
    """Очистить таблицы перед повторным импортом."""
    conn.execute("DELETE FROM appointments")
    conn.execute("DELETE FROM patients")
    conn.execute("DELETE FROM doctors")
    conn.execute("DELETE FROM specialties")


def import_specialties(conn):
    """Записать справочник специальностей."""
    conn.executemany(
        """
        INSERT INTO specialties (id, name)
        VALUES (?, ?)
        """,
        [
            (index, name)
            for index, name in enumerate(KNOWN_SPECIALTIES, start=1)
        ],
    )


def import_doctors(conn, doctors):
    """Записать врачей и связать их со специальностью."""
    rows = conn.execute("SELECT id, name FROM specialties").fetchall()
    specialty_ids = {row["name"]: row["id"] for row in rows}
    conn.executemany(
        """
        INSERT INTO doctors (id, name, specialty_id)
        VALUES (?, ?, ?)
        """,
        [
            (
                doctor["id"],
                doctor["name"],
                specialty_ids[doctor["specialty"]],
            )
            for doctor in doctors
        ],
    )


def import_patients_and_appointments(conn, appointments):
    """Выделить пациентов из записей и записать обе таблицы."""
    patients = []
    patient_ids = {}
    for item in appointments:
        key = (item["patient_name"], item["patient_age"])
        if key not in patient_ids:
            patient_ids[key] = len(patients) + 1
            patients.append(key)
    conn.executemany(
        """
        INSERT INTO patients (id, name, age)
        VALUES (?, ?, ?)
        """,
        [
            (index, name, age)
            for index, (name, age) in enumerate(patients, start=1)
        ],
    )
    conn.executemany(
        """
        INSERT INTO appointments (
            id,
            doctor_id,
            patient_id,
            appointment_date,
            appointment_time,
            is_cancelled
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item["id"],
                item["doctor_id"],
                patient_ids[(item["patient_name"], item["patient_age"])],
                item["appointment_date"],
                item["appointment_time"],
                int(item["is_cancelled"]),
            )
            for item in appointments
        ],
    )


def main():
    """Создать таблицы и перенести JSON в базу."""
    apply_schema()
    doctors = load_json(DOCTORS_FILE)
    appointments = load_json(APPOINTMENTS_FILE)
    conn = get_connection()
    try:
        clear_tables(conn)
        import_specialties(conn)
        import_doctors(conn, doctors)
        import_patients_and_appointments(conn, appointments)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
