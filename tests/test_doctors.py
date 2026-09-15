from doctors import add_doctor, filter_doctors_by_specialty, find_doctor


def test_add_doctor():
    doctors = {}
    add_doctor(doctors, "Смирнова Анна Сергеевна", "Терапевт")
    assert len(doctors) == 1


def test_find_doctor():
    doctors = {}
    add_doctor(doctors, "Смирнова Анна Сергеевна", "Терапевт")
    assert find_doctor(doctors, "смирнова")


def test_filter_doctors_by_specialty():
    doctors = {}
    add_doctor(doctors, "Петров Олег Викторович", "Кардиолог")
    assert filter_doctors_by_specialty(doctors, "Кардиолог")
