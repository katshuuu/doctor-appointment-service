"""Функции для работы с коллекцией записей на прием (List[Appointment])."""

from datetime import date, time

from entities.appointment import Appointment
from entities.doctor import Doctor
from entities.patient import Patient


def is_slot_available(
    appointments: list[Appointment],
    doctor: Doctor,
    appointment_date: date,
    appointment_time: time,
) -> bool:
    """Проверить, свободен ли врач на указанные дату и время.

    Учитываются только активные записи — отменённая запись
    (appointment.is_cancelled) время не блокирует.
    """
    for appointment in appointments:
        if (
            not appointment.is_cancelled
            and appointment.doctor.id == doctor.id
            and appointment.appointment_date == appointment_date
            and appointment.appointment_time == appointment_time
        ):
            return False
    return True


def create_appointment(
    appointments: list[Appointment],
    doctor: Doctor,
    patient: Patient,
    appointment_date: date,
    appointment_time: time,
) -> Appointment:
    """Создать новую запись на прием, связав её с объектами Doctor и Patient.

    Запись создается только если врач свободен на указанные дату
    и время, иначе выбрасывается исключение ValueError.
    """
    if not is_slot_available(
        appointments, doctor, appointment_date, appointment_time
    ):
        raise ValueError("Время уже занято")

    new_id = max((item.id for item in appointments), default=0) + 1
    appointment = Appointment(
        new_id, doctor, patient, appointment_date, appointment_time,
    )
    appointments.append(appointment)
    return appointment


def find_appointment_by_id(
    appointments: list[Appointment], appointment_id: int
) -> Appointment | None:
    """Найти запись по идентификатору."""
    for appointment in appointments:
        if appointment.id == appointment_id:
            return appointment
    return None


def cancel_appointment(
    appointments: list[Appointment], appointment_id: int
) -> None:
    """Отменить запись на прием по её идентификатору.

    Запись не удаляется: вызывается её метод Appointment.cancel(),
    изменяющий состояние объекта. Если запись с таким идентификатором
    не найдена, выбрасывается исключение ValueError.
    """
    appointment = find_appointment_by_id(appointments, appointment_id)
    if appointment is None:
        raise ValueError(f"Запись с id={appointment_id} не найдена")
    appointment.cancel()


def get_appointments_statistics(
    appointments: list[Appointment],
) -> dict[str, int]:
    """Подсчитать количество активных записей по каждому врачу."""
    statistics: dict[str, int] = {}
    for appointment in appointments:
        if appointment.is_cancelled:
            continue
        doctor_name = appointment.doctor.name
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


def show_appointments(appointments: list[Appointment]) -> None:
    """Вывести список всех записей на прием (активных и отменённых)."""
    if not appointments:
        print("Список записей пуст")
        return
    for appointment in appointments:
        print(appointment)
