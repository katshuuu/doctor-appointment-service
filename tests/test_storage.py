import json
from datetime import date, time

from appointments import create_appointment
from entities import Appointment, Doctor, Patient
from storage import (
    load_appointments,
    load_doctors,
    save_appointments,
    save_doctors,
)


def test_json_roundtrip(tmp_path) -> None:
    doctors_file = tmp_path / "doctors.json"
    appointments_file = tmp_path / "appointments.json"

    doctor = Doctor(1, "Смирнова Анна Сергеевна", "Терапевт")
    save_doctors(str(doctors_file), [doctor])
    loaded_doctors = load_doctors(str(doctors_file))

    appointments: list[Appointment] = []
    create_appointment(
        appointments,
        doctor,
        Patient("Иванов Иван Иванович", 34),
        date(2026, 9, 15),
        time(10, 30),
    )
    save_appointments(str(appointments_file), appointments)

    raw = json.loads(appointments_file.read_text(encoding="utf-8"))
    assert raw[0]["doctor_id"] == 1

    loaded = load_appointments(str(appointments_file), loaded_doctors)
    assert loaded[0].doctor is loaded_doctors[0]
    assert loaded[0].patient.name == "Иванов Иван Иванович"
