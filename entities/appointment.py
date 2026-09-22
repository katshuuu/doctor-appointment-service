"""Сущность «Запись» (на прием) — класс Appointment.

Запись связывает объект Doctor и объект Patient (композиция: запись
"владеет" пациентом и ссылается на врача) — именно то взаимодействие
объектов, которого требует методичка ПР3, а не просто перенос словаря
в класс.
"""

from datetime import date, time
from typing import Any

from entities.doctor import Doctor
from entities.patient import Patient


class Appointment:
    """Запись пациента на прием к врачу."""

    def __init__(
        self,
        appointment_id: int,
        doctor: Doctor,
        patient: Patient,
        appointment_date: date,
        appointment_time: time,
        is_cancelled: bool = False,
    ) -> None:
        """Создать объект записи на прием."""
        self.id = appointment_id
        self.doctor = doctor
        self.patient = patient
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.is_cancelled = is_cancelled

    def cancel(self) -> None:
        """Отменить запись.

        Запись не удаляется из коллекции — изменяется только её
        состояние. Отменённая запись перестаёт блокировать время
        приема (см. appointments.is_slot_available()).
        """
        self.is_cancelled = True

    def __str__(self) -> str:
        """Вернуть строковое представление записи с учетом её состояния."""
        status = "отменена" if self.is_cancelled else "активна"
        return (
            f"{self.id}. {self.patient.name} -> {self.doctor.name}, "
            f"{self.appointment_date} {self.appointment_time} ({status})"
        )

    @classmethod
    def from_data(cls, data: dict[str, Any], doctor: Doctor) -> "Appointment":
        """Создать запись из словаря JSON и уже найденного объекта врача.

        Поиск врача по doctor_id выполняется вызывающим кодом
        (storage.load_appointments()) в коллекции List[Doctor] — сама
        запись только связывает уже готовые объекты Doctor и Patient,
        как того требует методичка (раздел 5.4.9).
        """
        patient = Patient.from_data(data)
        return cls(
            data["id"],
            doctor,
            patient,
            date.fromisoformat(data["appointment_date"]),
            time.fromisoformat(data["appointment_time"]),
            data.get("is_cancelled", False),
        )
