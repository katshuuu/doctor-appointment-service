"""
Сервис записи к врачу. Точка запуска программы и основной сценарий.

Данные приложения хранятся в коллекциях doctors (словарь врачей) и
appointments (список записей на прием) и сохраняются в JSON-файлах.
Начальный сценарий ПР1 (пациент, врач, одна запись) переработан:
одиночные переменные заменены структурами данных, функциональность
разбита на модули doctors.py, appointments.py, storage.py, utils.py.
"""

from typing import Any

from appointments import (
    cancel_appointment,
    create_appointment,
    get_appointment_status,
    get_appointments_statistics,
    is_slot_available,
)
from doctors import (
    add_doctor,
    filter_doctors_by_specialty,
    find_doctor,
    sort_doctors,
)
from storage import (
    load_appointments,
    load_doctors,
    save_appointments,
    save_doctors,
)
from utils import convert_age, input_date, input_int, input_time

DOCTORS_FILE = "data/doctors.json"
APPOINTMENTS_FILE = "data/appointments.json"


def show_doctors(doctors: dict[int, dict[str, Any]]) -> None:
    """Вывести список врачей в виде таблицы."""
    if not doctors:
        print("Список врачей пуст")
        return
    for doctor_id, doctor_data in sort_doctors(doctors):
        print(
            f"{doctor_id}. {doctor_data['name']} — "
            f"{doctor_data['specialty']}"
        )


def show_appointments(
    appointments: list[dict[str, Any]], doctors: dict[int, dict[str, Any]]
) -> None:
    """Вывести список записей на прием."""
    if not appointments:
        print("Список записей пуст")
        return
    for appointment in appointments:
        doctor = doctors.get(appointment["doctor_id"], {})
        doctor_name = doctor.get("name", "неизвестный врач")
        print(
            f"{appointment['id']}. {appointment['patient_name']} "
            f"({appointment['patient_age']} лет) -> {doctor_name}, "
            f"{appointment['appointment_date']} "
            f"{appointment['appointment_time']}"
        )


def build_appointment_summary(
    patient_name: str,
    patient_age: int,
    doctor_name: str,
    specialty: str,
    appointment_date: str,
    appointment_time: str,
    status: str,
) -> str:
    """Сформировать итоговый текст о записи (функция из ПР1, без изменений)."""
    return (
        f"Пациент: {patient_name}, возраст: {patient_age}\n"
        f"Врач: {doctor_name}\n"
        f"Специальность: {specialty}\n"
        f"Дата приема: {appointment_date}, время: {appointment_time}\n"
        f"{status}"
    )


def show_statistics(
    appointments: list[dict[str, Any]], doctors: dict[int, dict[str, Any]]
) -> None:
    """Вывести статистику количества записей по врачам."""
    statistics = get_appointments_statistics(appointments, doctors)
    if not statistics:
        print("Записей пока нет")
        return
    for doctor_name, count in statistics.items():
        print(f"{doctor_name}: {count} записей")


def _print_menu() -> None:
    print("\n=== Сервис записи к врачу ===")
    print("1. Показать врачей")
    print("2. Найти врача по имени")
    print("3. Показать врачей по специальности")
    print("4. Проверить доступность времени")
    print("5. Записаться на прием")
    print("6. Отменить запись")
    print("7. Показать записи")
    print("8. Показать статистику записей")
    print("0. Выход")


def main() -> None:
    """Точка запуска приложения: меню и вызов функций проекта."""
    doctors = load_doctors(DOCTORS_FILE)
    appointments = load_appointments(APPOINTMENTS_FILE)
    if not doctors:
        add_doctor(doctors, "Смирнова Анна Сергеевна", "Терапевт")
        add_doctor(doctors, "Петров Олег Викторович", "Кардиолог")
        save_doctors(DOCTORS_FILE, doctors)

    while True:
        _print_menu()
        choice = input("Выберите действие: ")

        if choice == "1":
            show_doctors(doctors)

        elif choice == "2":
            query = input("Введите часть имени врача: ")
            found = find_doctor(doctors, query)
            show_doctors(found)

        elif choice == "3":
            specialty = input("Специальность: ")
            found = filter_doctors_by_specialty(doctors, specialty)
            show_doctors(found)

        elif choice == "4":
            doctor_id = input_int("ID врача: ")
            appointment_date = input_date("Дата (ДД.ММ.ГГГГ): ")
            appointment_time = input_time("Время (ЧЧ:ММ): ")
            available = is_slot_available(
                appointments, doctor_id, appointment_date, appointment_time
            )
            print(get_appointment_status(available, is_minor_patient=False))

        elif choice == "5":
            doctor_id = input_int("ID врача: ")
            doctor = doctors.get(doctor_id)
            if doctor is None:
                print("Врач с таким ID не найден")
                continue
            patient_name = input("ФИО пациента: ")
            patient_age = convert_age(input("Возраст пациента: "))
            appointment_date = input_date("Дата (ДД.ММ.ГГГГ): ")
            appointment_time = input_time("Время (ЧЧ:ММ): ")
            is_minor_patient = patient_age < 18
            available = is_slot_available(
                appointments, doctor_id, appointment_date, appointment_time
            )
            status = get_appointment_status(available, is_minor_patient)
            try:
                create_appointment(
                    appointments, doctor_id, patient_name, patient_age,
                    appointment_date, appointment_time,
                )
                save_appointments(APPOINTMENTS_FILE, appointments)
            except ValueError as error:
                status = str(error)
            print(build_appointment_summary(
                patient_name, patient_age, doctor["name"], doctor["specialty"],
                appointment_date, appointment_time, status,
            ))

        elif choice == "6":
            appointment_id = input_int("ID записи для отмены: ")
            try:
                cancel_appointment(appointments, appointment_id)
                save_appointments(APPOINTMENTS_FILE, appointments)
                print("Запись отменена")
            except ValueError as error:
                print(error)

        elif choice == "7":
            show_appointments(appointments, doctors)

        elif choice == "8":
            show_statistics(appointments, doctors)

        elif choice == "0":
            save_doctors(DOCTORS_FILE, doctors)
            save_appointments(APPOINTMENTS_FILE, appointments)
            print("До свидания!")
            break

        else:
            print("Неизвестный пункт меню")


if __name__ == "__main__":
    main()
