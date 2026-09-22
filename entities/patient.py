"""Сущность «Пациент» — класс Patient.

До ПР3 пациент существовал только как пара полей внутри словаря записи
(ПР2). В ПР3 пациент выделен в собственный класс — ровно так, как
методические указания к ПР3 предписывают выделять сущность, у которой
есть собственные данные и операции (проверка возраста), даже если
отдельного JSON-файла и коллекции пациентов в проекте не заводится:
данные пациента по-прежнему хранятся внутри записи на прием.
"""

from typing import Any

MINOR_AGE_LIMIT = 18


class Patient:
    """Пациент, записывающийся на прием к врачу."""

    def __init__(self, name: str, age: int) -> None:
        """Создать объект пациента."""
        self.name = name
        self.age = age

    def __str__(self) -> str:
        """Вернуть строковое представление пациента."""
        return f"{self.name}, {self.age} лет"

    def is_minor(self) -> bool:
        """Проверить, является ли пациент несовершеннолетним."""
        return self.is_minor_age(self.age)

    @staticmethod
    def is_minor_age(age: int) -> bool:
        """Проверить, соответствует ли возраст несовершеннолетнему.

        Статический метод: логически относится к классу Patient
        (правило "несовершеннолетний — младше 18"), но не использует
        данные конкретного объекта, поэтому не принимает self и может
        вызываться напрямую через класс: Patient.is_minor_age(16).
        """
        return age < MINOR_AGE_LIMIT

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Patient":
        """Создать пациента из словаря данных записи на прием.

        Ключи patient_name/patient_age берутся из формата хранения
        appointments.json (см. entities/appointment.py и storage.py).
        """
        return cls(data["patient_name"], data["patient_age"])
