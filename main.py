"""
Сервис записи к врачу
ПР1. Начальный сценарий: проверка возможности записи пациента на прием.

Сущности предметной области: пациент, врач, специальность, запись.
На данном этапе используются только простые типы данных, операции,
преобразование типов, ветвления и импорт модуля (без коллекций и циклов —
они будут добавлены на ПР2).
"""

from datetime import date, time

# --- Данные пациента (простые типы данных) ---
patient_name = "Иванов Иван Иванович"
patient_age_input = "34"          # значение получено, например, из формы записи (строка)
patient_age = int(patient_age_input)  # преобразование типов: str -> int

# --- Данные врача и специальности ---
doctor_name = "Смирнова Анна Сергеевна"
specialty = "Терапевт"

# --- Данные записи (appointment) ---
appointment_date = date(2026, 9, 15)
appointment_time = time(10, 30)
slot_is_free = True

# --- Операции и логическое условие ---
is_minor_patient = patient_age < 18  # операция сравнения


def get_appointment_status(slot_is_free, is_minor_patient):
    """Определяет статус записи на основании занятости слота и возраста пациента."""
    if slot_is_free and not is_minor_patient:
        return "Запись подтверждена"
    elif slot_is_free and is_minor_patient:
        return "Запись подтверждена. Требуется присутствие законного представителя"
    else:
        return "Время занято. Пожалуйста, выберите другой слот"


# --- Вывод результата ---
print(f"Пациент: {patient_name}, возраст: {patient_age}")
print(f"Врач: {doctor_name}")
print(f"Специальность: {specialty}")
print(f"Дата приема: {appointment_date}, время: {appointment_time}")
print(get_appointment_status(slot_is_free, is_minor_patient))
