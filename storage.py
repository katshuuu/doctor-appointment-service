"""Функции сохранения и загрузки данных проекта в JSON-файлах.

Модуль отвечает за преобразование: JSON -> объекты (при загрузке) и
объекты -> JSON (при сохранении). Сами объекты Doctor, Patient и
Appointment ничего не знают про файлы — это принципиально разделено
(см. подраздел 5.1.5 методических указаний ПР3).
"""

import json
from typing import Any

from doctors import find_doctor_by_id
from entities.appointment import Appointment
from entities.doctor import Doctor


def load_doctors(filename: str) -> list[Doctor]:
    """Загрузить врачей из JSON-файла и создать объекты Doctor.

    При отсутствии файла или повреждении JSON возвращает пустой список.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} поврежден, данные не загружены")
        return []
    return [Doctor.from_data(item) for item in data]


def save_doctors(filename: str, doctors: list[Doctor]) -> None:
    """Сохранить объекты Doctor в JSON-файл."""
    data = [
        {"id": doctor.id, "name": doctor.name, "specialty": doctor.specialty}
        for doctor in doctors
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_appointments(
    filename: str, doctors: list[Doctor]
) -> list[Appointment]:
    """Загрузить записи на прием из JSON-файла и создать объекты Appointment.

    Для каждой записи по doctor_id ищется соответствующий объект Doctor
    в уже загруженной коллекции doctors. Если врач не найден, запись
    пропускается (некорректная связь не должна создавать объект) — об
    этом выводится предупреждение, само чтение файла не прерывается.
    При отсутствии файла или повреждении JSON возвращается пустой список.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} поврежден, данные не загружены")
        return []

    appointments: list[Appointment] = []
    for item in data:
        doctor = find_doctor_by_id(doctors, item["doctor_id"])
        if doctor is None:
            print(
                f"Запись id={item['id']}: врач id={item['doctor_id']} "
                "не найден, запись пропущена"
            )
            continue
        appointments.append(Appointment.from_data(item, doctor))
    return appointments


def save_appointments(
    filename: str, appointments: list[Appointment]
) -> None:
    """Сохранить объекты Appointment в JSON-файл.

    Связанный объект Doctor сохраняется как doctor_id (идентификатор),
    а не как вложенная структура — см. раздел 5.4.9 методических
    указаний ПР3.
    """
    data: list[dict[str, Any]] = [
        {
            "id": appointment.id,
            "doctor_id": appointment.doctor.id,
            "patient_name": appointment.patient.name,
            "patient_age": appointment.patient.age,
            "appointment_date": appointment.appointment_date.isoformat(),
            "appointment_time": appointment.appointment_time.isoformat(),
            "is_cancelled": appointment.is_cancelled,
        }
        for appointment in appointments
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
