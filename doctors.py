"""Функции для работы с коллекцией врачей (List[Doctor])."""

from typing import Iterator

from entities.doctor import Doctor


def add_doctor(doctors: list[Doctor], name: str, specialty: str) -> Doctor:
    """Создать объект Doctor, добавить его в коллекцию и вернуть его."""
    new_id = max((doctor.id for doctor in doctors), default=0) + 1
    doctor = Doctor(new_id, name, specialty)
    doctors.append(doctor)
    return doctor


def find_doctor_by_id(
    doctors: list[Doctor], doctor_id: int
) -> Doctor | None:
    """Найти врача по идентификатору."""
    for doctor in doctors:
        if doctor.id == doctor_id:
            return doctor
    return None


def find_doctor(doctors: list[Doctor], query: str) -> list[Doctor]:
    """Найти врачей по подстроке имени (без учета регистра)."""
    query = query.lower()
    return [doctor for doctor in doctors if query in doctor.name.lower()]


def check_doctor_specialty(
    doctors: list[Doctor], doctor_id: int, specialty: str
) -> bool:
    """Проверить, работает ли врач по указанной специальности."""
    doctor = find_doctor_by_id(doctors, doctor_id)
    if doctor is None:
        return False
    return doctor.specialty.lower() == specialty.lower()


def iter_doctors_by_specialty(
    doctors: list[Doctor], specialty: str
) -> Iterator[Doctor]:
    """Перебрать врачей заданной специальности (генератор)."""
    specialty = specialty.lower()
    for doctor in doctors:
        if doctor.specialty.lower() == specialty:
            yield doctor


def filter_doctors_by_specialty(
    doctors: list[Doctor], specialty: str
) -> list[Doctor]:
    """Отобрать врачей по специальности."""
    return list(iter_doctors_by_specialty(doctors, specialty))


def sort_doctors(doctors: list[Doctor]) -> list[Doctor]:
    """Отсортировать врачей по имени."""
    return sorted(doctors, key=lambda doctor: doctor.name)


def show_doctors(doctors: list[Doctor]) -> None:
    """Вывести список врачей в виде таблицы."""
    if not doctors:
        print("Список врачей пуст")
        return
    for doctor in sort_doctors(doctors):
        print(f"{doctor.id}. {doctor}")
