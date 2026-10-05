"""Загрузка объектов ПР3 для страниц веб-интерфейса."""

from urllib.parse import quote

from django.conf import settings

from storage import load_appointments, load_doctors


def load_domain():
    """Загрузить врачей и записи и восстановить связи объектов."""
    data_dir = settings.BASE_DIR / "data"
    doctors = load_doctors(str(data_dir / "doctors.json"))
    appointments = load_appointments(
        str(data_dir / "appointments.json"),
        doctors,
    )
    return doctors, appointments


def specialty_path(specialty):
    """Адрес страницы специальности."""
    return "/specialties/" + quote(specialty, safe="") + "/"
