"""Сущность «Врач» — класс Doctor."""

from typing import Any


class Doctor:
    """Врач, ведущий прием пациентов по своей специальности."""

    def __init__(self, doctor_id: int, name: str, specialty: str) -> None:
        """Создать объект врача."""
        self.id = doctor_id
        self.name = name
        self.specialty = specialty

    def __str__(self) -> str:
        """Вернуть строковое представление врача."""
        return f"{self.name} — {self.specialty}"

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Doctor":
        """Создать врача из словаря данных (например, из JSON)."""
        return cls(data["id"], data["name"], data["specialty"])
