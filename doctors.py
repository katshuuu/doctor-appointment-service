"""Функции для работы с врачами."""

from typing import Any


def add_doctor(
    doctors: dict[int, dict[str, Any]],
    doctor_name: str,
    specialty: str,
) -> None:
    """Добавить врача в словарь doctors.

    Идентификатор врача формируется автоматически.
    """
    new_id = max(doctors.keys(), default=0) + 1
    doctors[new_id] = {"name": doctor_name, "specialty": specialty}


def find_doctor(
    doctors: dict[int, dict[str, Any]], query: str
) -> dict[int, dict[str, Any]]:
    """Найти врачей по подстроке имени (без учета регистра)."""
    query = query.lower()
    return {
        doctor_id: doctor_data
        for doctor_id, doctor_data in doctors.items()
        if query in doctor_data["name"].lower()
    }


def check_doctor_specialty(
    doctors: dict[int, dict[str, Any]],
    doctor_id: int,
    specialty: str,
) -> bool:
    """Проверить, работает ли врач по указанной специальности."""
    doctor = doctors.get(doctor_id)
    if doctor is None:
        return False
    return doctor["specialty"].lower() == specialty.lower()


def iter_doctors_by_specialty(
    doctors: dict[int, dict[str, Any]], specialty: str
):
    """Перебрать врачей заданной специальности (генератор).

    Используется вместо промежуточного списка там, где элементы
    нужно только перебрать, а не хранить целиком.
    """
    for doctor_id, doctor_data in doctors.items():
        if check_doctor_specialty(doctors, doctor_id, specialty):
            yield doctor_id, doctor_data


def filter_doctors_by_specialty(
    doctors: dict[int, dict[str, Any]], specialty: str
) -> dict[int, dict[str, Any]]:
    """Отобрать врачей по специальности."""
    return dict(iter_doctors_by_specialty(doctors, specialty))


def sort_doctors(
    doctors: dict[int, dict[str, Any]]
) -> list[tuple[int, dict[str, Any]]]:
    """Отсортировать врачей по имени."""
    return sorted(doctors.items(), key=lambda item: item[1]["name"])
