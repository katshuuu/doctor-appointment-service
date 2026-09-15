"""Функции для создания и проверки записей на прием."""

from datetime import date, time
from typing import Any


def is_slot_available(
    appointments: list[dict[str, Any]],
    doctor_id: int,
    appointment_date: date,
    appointment_time: time,
) -> bool:
    """Проверить, свободен ли врач на указанные дату и время."""
    for appointment in appointments:
        if (
            appointment["doctor_id"] == doctor_id
            and appointment["appointment_date"] == appointment_date.isoformat()
            and appointment["appointment_time"] == appointment_time.isoformat()
        ):
            return False
    return True


def create_appointment(
    appointments: list[dict[str, Any]],
    doctor_id: int,
    patient_name: str,
    patient_age: int,
    appointment_date: date,
    appointment_time: time,
) -> dict[str, Any]:
    """Создать новую запись на прием.

    Запись создается только если врач свободен на указанные дату
    и время, иначе выбрасывается исключение ValueError.
    """
    if not is_slot_available(
        appointments, doctor_id, appointment_date, appointment_time
    ):
        raise ValueError("Время уже занято")

    new_id = max((item["id"] for item in appointments), default=0) + 1
    appointment = {
        "id": new_id,
        "doctor_id": doctor_id,
        "patient_name": patient_name,
        "patient_age": patient_age,
        "appointment_date": appointment_date.isoformat(),
        "appointment_time": appointment_time.isoformat(),
    }
    appointments.append(appointment)
    return appointment


def cancel_appointment(
    appointments: list[dict[str, Any]], appointment_id: int
) -> None:
    """Отменить запись на прием по ее идентификатору.

    Если запись с таким идентификатором не найдена, выбрасывается
    исключение ValueError.
    """
    for index, appointment in enumerate(appointments):
        if appointment["id"] == appointment_id:
            del appointments[index]
            return
    raise ValueError(f"Запись с id={appointment_id} не найдена")


def get_appointments_statistics(
    appointments: list[dict[str, Any]],
    doctors: dict[int, dict[str, Any]],
) -> dict[str, int]:
    """Подсчитать количество записей на прием по каждому врачу."""
    statistics: dict[str, int] = {}
    for appointment in appointments:
        doctor = doctors.get(appointment["doctor_id"], {})
        doctor_name = doctor.get("name", "неизвестный врач")
        statistics[doctor_name] = statistics.get(doctor_name, 0) + 1
    return statistics


def get_appointment_status(slot_is_free: bool, is_minor_patient: bool) -> str:
    """Определить статус записи на прием (функция из ПР1, без изменений)."""
    if slot_is_free and not is_minor_patient:
        return "Запись подтверждена"
    elif slot_is_free and is_minor_patient:
        return (
            "Запись подтверждена. "
            "Требуется присутствие законного представителя"
        )
    else:
        return "Время занято. Пожалуйста, выберите другой слот"
