import json
from datetime import date, time
from pathlib import Path

from appointments import create_appointment
from entities import Appointment, Doctor, Patient
from storage import (
    load_appointments,
    load_doctors,
    save_appointments,
    save_doctors,
)


def test_json_roundtrip(tmp_path) -> None:
    doctors_file = tmp_path / "doctors.json"
    appointments_file = tmp_path / "appointments.json"

    doctor = Doctor(1, "Смирнова Анна Сергеевна", "Терапевт")
    save_doctors(str(doctors_file), [doctor])
    loaded_doctors = load_doctors(str(doctors_file))

    appointments: list[Appointment] = []
    create_appointment(
        appointments,
        doctor,
        Patient("Иванов Иван Иванович", 34),
        date(2026, 9, 15),
        time(10, 30),
    )
    save_appointments(str(appointments_file), appointments)

    raw = json.loads(appointments_file.read_text(encoding="utf-8"))
    assert raw[0]["doctor_id"] == 1

    loaded = load_appointments(str(appointments_file), loaded_doctors)
    assert loaded[0].doctor is loaded_doctors[0]
    assert loaded[0].patient.name == "Иванов Иван Иванович"


def test_project_data_matches_assignment() -> None:
    """Исходные JSON содержат 15 врачей и 15 записей из задания ПР3."""
    root = Path(__file__).resolve().parents[1]
    doctors = load_doctors(str(root / "data" / "doctors.json"))
    appointments = load_appointments(
        str(root / "data" / "appointments.json"), doctors
    )

    assert [doctor.name for doctor in doctors] == [
        "Смирнова Анна Сергеевна",
        "Петров Олег Викторович",
        "Кузнецов Дмитрий Андреевич",
        "Волкова Елена Ивановна",
        "Морозов Игорь Петрович",
        "Новикова Ольга Владимировна",
        "Соколов Артём Николаевич",
        "Павлова Мария Дмитриевна",
        "Фёдоров Сергей Алексеевич",
        "Егорова Наталья Павловна",
        "Лебедев Виктор Станиславович",
        "Козлова Виктория Романовна",
        "Тихонов Михаил Юрьевич",
        "Сидорова Татьяна Борисовна",
        "Громов Андрей Валерьевич",
    ]
    assert [doctor.specialty for doctor in doctors] == [
        "Терапевт",
        "Кардиолог",
        "Невролог",
        "Педиатр",
        "Хирург",
        "Офтальмолог",
        "Стоматолог",
        "Дерматолог",
        "Уролог",
        "Эндокринолог",
        "Оториноларинголог",
        "Гинеколог",
        "Психиатр",
        "Аллерголог",
        "Онколог",
    ]
    assert len(appointments) == 15
    assert appointments[0].patient.name == "Иванов Иван Иванович"
    assert appointments[0].patient.age == 34
    assert appointments[0].doctor is doctors[0]
    assert appointments[0].appointment_date == date(2026, 9, 15)
    assert appointments[0].appointment_time == time(10, 30)
    assert {item.id for item in appointments if item.is_cancelled} == {
        3, 7, 12,
    }
    assert appointments[14].patient.name == "Тихонов Михаил Юрьевич"
    assert appointments[14].doctor is doctors[4]
