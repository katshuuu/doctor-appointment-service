from doctors import (
    add_doctor,
    check_doctor_specialty,
    filter_doctors_by_specialty,
    find_doctor,
    find_doctor_by_id,
    sort_doctors,
)
from entities.doctor import Doctor


def test_doctor_creation():
    doctor = Doctor(1, "Смирнова Анна Сергеевна", "Терапевт")

    assert doctor.id == 1
    assert doctor.name == "Смирнова Анна Сергеевна"
    assert doctor.specialty == "Терапевт"


def test_doctor_str():
    doctor = Doctor(1, "Смирнова Анна Сергеевна", "Терапевт")

    assert str(doctor) == "Смирнова Анна Сергеевна — Терапевт"


def test_doctor_from_data():
    doctor = Doctor.from_data(
        {"id": 2, "name": "Петров Олег Викторович", "specialty": "Кардиолог"}
    )

    assert doctor.id == 2
    assert doctor.specialty == "Кардиолог"


def test_add_doctor():
    doctors: list[Doctor] = []
    add_doctor(doctors, "Смирнова Анна Сергеевна", "Терапевт")

    assert len(doctors) == 1
    assert doctors[0].name == "Смирнова Анна Сергеевна"


def test_find_doctor_by_id():
    doctors: list[Doctor] = []
    doctor = add_doctor(doctors, "Смирнова Анна Сергеевна", "Терапевт")

    assert find_doctor_by_id(doctors, doctor.id) is doctor
    assert find_doctor_by_id(doctors, 999) is None


def test_find_doctor():
    doctors: list[Doctor] = []
    add_doctor(doctors, "Смирнова Анна Сергеевна", "Терапевт")

    found = find_doctor(doctors, "смирнова")

    assert len(found) == 1
    assert found[0].name == "Смирнова Анна Сергеевна"


def test_check_doctor_specialty():
    doctors: list[Doctor] = []
    doctor = add_doctor(doctors, "Петров Олег Викторович", "Кардиолог")

    assert check_doctor_specialty(doctors, doctor.id, "кардиолог")
    assert not check_doctor_specialty(doctors, doctor.id, "терапевт")


def test_filter_doctors_by_specialty():
    doctors: list[Doctor] = []
    add_doctor(doctors, "Петров Олег Викторович", "Кардиолог")
    add_doctor(doctors, "Смирнова Анна Сергеевна", "Терапевт")

    found = filter_doctors_by_specialty(doctors, "Кардиолог")

    assert len(found) == 1
    assert found[0].specialty == "Кардиолог"


def test_sort_doctors():
    doctors: list[Doctor] = []
    add_doctor(doctors, "Смирнова Анна Сергеевна", "Терапевт")
    add_doctor(doctors, "Петров Олег Викторович", "Кардиолог")

    sorted_doctors = sort_doctors(doctors)

    assert [doctor.name for doctor in sorted_doctors] == [
        "Петров Олег Викторович", "Смирнова Анна Сергеевна",
    ]
