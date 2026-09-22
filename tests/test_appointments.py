from datetime import date, time

from appointments import (
    cancel_appointment,
    create_appointment,
    find_appointment_by_id,
    get_appointments_statistics,
    is_slot_available,
)
from entities.appointment import Appointment
from entities.doctor import Doctor
from entities.patient import Patient


def _doctor() -> Doctor:
    return Doctor(1, "Смирнова Анна Сергеевна", "Терапевт")


def test_appointment_creation_links_doctor_and_patient():
    doctor = _doctor()
    patient = Patient("Иванов Иван Иванович", 34)
    appointment = Appointment(
        1, doctor, patient, date(2026, 9, 15), time(10, 30),
    )

    assert appointment.id == 1
    assert appointment.doctor is doctor
    assert appointment.patient is patient
    assert not appointment.is_cancelled


def test_appointment_cancel_changes_state_without_removal():
    doctor = _doctor()
    patient = Patient("Иванов Иван Иванович", 34)
    appointment = Appointment(
        1, doctor, patient, date(2026, 9, 15), time(10, 30),
    )

    appointment.cancel()

    assert appointment.is_cancelled
    assert appointment.doctor is doctor


def test_appointment_str_reflects_status():
    doctor = _doctor()
    patient = Patient("Иванов Иван Иванович", 34)
    appointment = Appointment(
        1, doctor, patient, date(2026, 9, 15), time(10, 30),
    )

    assert "активна" in str(appointment)
    appointment.cancel()
    assert "отменена" in str(appointment)


def test_appointment_from_data():
    doctor = _doctor()
    appointment = Appointment.from_data(
        {
            "id": 1,
            "patient_name": "Иванов Иван Иванович",
            "patient_age": 34,
            "appointment_date": "2026-09-15",
            "appointment_time": "10:30:00",
            "is_cancelled": False,
        },
        doctor,
    )

    assert appointment.doctor is doctor
    assert appointment.patient.name == "Иванов Иван Иванович"
    assert appointment.appointment_date == date(2026, 9, 15)


def test_is_slot_available():
    appointments: list[Appointment] = []
    doctor = _doctor()

    assert is_slot_available(
        appointments, doctor, date(2026, 9, 15), time(10, 30)
    )


def test_duplicate_appointment_forbidden():
    appointments: list[Appointment] = []
    doctor = _doctor()
    create_appointment(
        appointments, doctor, Patient("Иванов Иван Иванович", 34),
        date(2026, 9, 15), time(10, 30),
    )

    assert not is_slot_available(
        appointments, doctor, date(2026, 9, 15), time(10, 30)
    )


def test_cancelled_appointment_frees_the_slot():
    appointments: list[Appointment] = []
    doctor = _doctor()
    appointment = create_appointment(
        appointments, doctor, Patient("Иванов Иван Иванович", 34),
        date(2026, 9, 15), time(10, 30),
    )

    appointment.cancel()

    assert is_slot_available(
        appointments, doctor, date(2026, 9, 15), time(10, 30)
    )


def test_cancel_appointment_keeps_it_in_collection():
    appointments: list[Appointment] = []
    doctor = _doctor()
    appointment = create_appointment(
        appointments, doctor, Patient("Иванов Иван Иванович", 34),
        date(2026, 9, 15), time(10, 30),
    )

    cancel_appointment(appointments, appointment.id)

    assert len(appointments) == 1
    assert appointments[0].is_cancelled


def test_cancel_unknown_appointment_raises_value_error():
    appointments: list[Appointment] = []

    try:
        cancel_appointment(appointments, 999)
        assert False, "ожидалось исключение ValueError"
    except ValueError:
        pass


def test_find_appointment_by_id():
    appointments: list[Appointment] = []
    doctor = _doctor()
    appointment = create_appointment(
        appointments, doctor, Patient("Иванов Иван Иванович", 34),
        date(2026, 9, 15), time(10, 30),
    )

    assert find_appointment_by_id(appointments, appointment.id) is appointment
    assert find_appointment_by_id(appointments, 999) is None


def test_get_appointments_statistics_counts_only_active():
    appointments: list[Appointment] = []
    doctor = _doctor()
    create_appointment(
        appointments, doctor, Patient("Иванов Иван Иванович", 34),
        date(2026, 9, 15), time(10, 30),
    )
    cancelled = create_appointment(
        appointments, doctor, Patient("Петрова Анна Сергеевна", 28),
        date(2026, 9, 15), time(11, 0),
    )
    cancelled.cancel()

    statistics = get_appointments_statistics(appointments)

    assert statistics == {"Смирнова Анна Сергеевна": 1}
