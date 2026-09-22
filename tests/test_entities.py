from entities.patient import Patient
from entities.specialty import is_known_specialty


def test_patient_creation_and_str():
    patient = Patient("Иванов Иван Иванович", 34)

    assert patient.name == "Иванов Иван Иванович"
    assert patient.age == 34
    assert str(patient) == "Иванов Иван Иванович, 34 лет"


def test_patient_is_minor():
    adult = Patient("Иванов Иван Иванович", 34)
    minor = Patient("Петров Петр Петрович", 15)

    assert not adult.is_minor()
    assert minor.is_minor()


def test_patient_is_minor_age_staticmethod():
    assert Patient.is_minor_age(15)
    assert not Patient.is_minor_age(18)


def test_patient_from_data():
    patient = Patient.from_data(
        {"patient_name": "Иванов Иван Иванович", "patient_age": 34}
    )

    assert patient.name == "Иванов Иван Иванович"
    assert patient.age == 34


def test_is_known_specialty():
    assert is_known_specialty("Терапевт")
    assert not is_known_specialty("Алхимик")
