"""Сущности предметной области проекта «Сервис записи к врачу».

Пакет объединяет классы предметной области, чтобы их можно было
импортировать напрямую из пакета:

    from entities import Doctor, Patient, Appointment

Всего 4 сущности — по одной на файл:
    doctor.py        — Doctor (Врач);
    patient.py        — Patient (Пациент);
    specialty.py       — справочник специальностей (Специальность);
    appointment.py     — Appointment (Запись на прием), связывающий
                          объекты Doctor и Patient.
"""

from entities.appointment import Appointment
from entities.doctor import Doctor
from entities.patient import Patient

__all__ = ["Doctor", "Patient", "Appointment"]
