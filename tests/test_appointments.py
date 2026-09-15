from datetime import date, time

from appointments import (
    cancel_appointment,
    create_appointment,
    get_appointments_statistics,
    is_slot_available,
)


def test_is_slot_available():
    appointments = []
    assert is_slot_available(appointments, 1, date(2026, 9, 15), time(10, 30))


def test_duplicate_appointment_forbidden():
    appointments = []
    create_appointment(
        appointments, 1, "Иванов Иван Иванович", 34,
        date(2026, 9, 15), time(10, 30),
    )
    assert not is_slot_available(
        appointments, 1, date(2026, 9, 15), time(10, 30)
    )


def test_cancel_appointment():
    appointments = []
    appointment = create_appointment(
        appointments, 1, "Иванов Иван Иванович", 34,
        date(2026, 9, 15), time(10, 30),
    )
    cancel_appointment(appointments, appointment["id"])
    assert appointments == []


def test_get_appointments_statistics():
    appointments = []
    doctors = {1: {"name": "Смирнова Анна Сергеевна", "specialty": "Терапевт"}}
    create_appointment(
        appointments, 1, "Иванов Иван Иванович", 34,
        date(2026, 9, 15), time(10, 30),
    )
    statistics = get_appointments_statistics(appointments, doctors)
    assert statistics == {"Смирнова Анна Сергеевна": 1}
