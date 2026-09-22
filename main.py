"""
Сервис записи к врачу. Точка запуска программы и основной сценарий.

После ПР3 приложение работает с объектами предметной области —
List[Doctor] и List[Appointment] (см. пакет entities/) — вместо
коллекций словарей ПР2. main.py не хранит и не обрабатывает словари
предметной области самостоятельно: вся логика вынесена в doctors.py,
appointments.py и storage.py, а main.py лишь организует пользовательский
сценарий и взаимодействие объектов.
"""

from appointments import (
    cancel_appointment,
    create_appointment,
    get_appointment_status,
    get_appointments_statistics,
    is_slot_available,
    show_appointments,
)
from doctors import (
    add_doctor,
    filter_doctors_by_specialty,
    find_doctor,
    find_doctor_by_id,
    show_doctors,
)
from entities import Appointment, Doctor, Patient
from storage import (
    load_appointments,
    load_doctors,
    save_appointments,
    save_doctors,
)
from utils import convert_age, input_date, input_int, input_time

DOCTORS_FILE = "data/doctors.json"
APPOINTMENTS_FILE = "data/appointments.json"


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


def show_statistics(appointments: list[Appointment]) -> None:
    """Вывести статистику количества активных записей по врачам."""
    statistics = get_appointments_statistics(appointments)
    if not statistics:
        print("Активных записей пока нет")
        return
    for doctor_name, count in statistics.items():
        print(f"{doctor_name}: {count} записей")


def create_new_appointment(
    doctors: list[Doctor], appointments: list[Appointment]
) -> None:
    """Провести пользовательский сценарий записи на прием.

    Находит объект Doctor по введённому ID, создает объект Patient,
    проверяет доступность времени и вызывает create_appointment(),
    которая связывает найденного врача с новой записью.
    """
    doctor_id = input_int("ID врача: ")
    doctor = find_doctor_by_id(doctors, doctor_id)
    if doctor is None:
        print("Врач с таким ID не найден")
        return

    patient_name = input("ФИО пациента: ")
    patient_age = convert_age(input("Возраст пациента: "))
    appointment_date = input_date("Дата (ДД.ММ.ГГГГ): ")
    appointment_time = input_time("Время (ЧЧ:ММ): ")
    patient = Patient(patient_name, patient_age)

    is_minor_patient = Patient.is_minor_age(patient_age)
    available = is_slot_available(
        appointments, doctor, appointment_date, appointment_time
    )
    status = get_appointment_status(available, is_minor_patient)
    try:
        create_appointment(
            appointments, doctor, patient,
            appointment_date, appointment_time,
        )
        save_appointments(APPOINTMENTS_FILE, appointments)
    except ValueError as error:
        status = str(error)

    print(build_appointment_summary(
        patient_name, patient_age, doctor.name, doctor.specialty,
        appointment_date.isoformat(), appointment_time.isoformat(),
        status,
    ))


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
    appointments = load_appointments(APPOINTMENTS_FILE, doctors)
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
            show_doctors(find_doctor(doctors, query))

        elif choice == "3":
            specialty = input("Специальность: ")
            show_doctors(filter_doctors_by_specialty(doctors, specialty))

        elif choice == "4":
            doctor_id = input_int("ID врача: ")
            doctor = find_doctor_by_id(doctors, doctor_id)
            if doctor is None:
                print("Врач с таким ID не найден")
                continue
            appointment_date = input_date("Дата (ДД.ММ.ГГГГ): ")
            appointment_time = input_time("Время (ЧЧ:ММ): ")
            available = is_slot_available(
                appointments, doctor, appointment_date, appointment_time
            )
            print(get_appointment_status(available, is_minor_patient=False))

        elif choice == "5":
            create_new_appointment(doctors, appointments)

        elif choice == "6":
            appointment_id = input_int("ID записи для отмены: ")
            try:
                cancel_appointment(appointments, appointment_id)
                save_appointments(APPOINTMENTS_FILE, appointments)
                print("Запись отменена")
            except ValueError as error:
                print(error)

        elif choice == "7":
            show_appointments(appointments)

        elif choice == "8":
            show_statistics(appointments)

        elif choice == "0":
            save_doctors(DOCTORS_FILE, doctors)
            save_appointments(APPOINTMENTS_FILE, appointments)
            print("До свидания!")
            break

        else:
            print("Неизвестный пункт меню")


if __name__ == "__main__":
    main()
