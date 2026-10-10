"""Проверка страниц веб-интерфейса ПР5."""

import os

import pytest

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "appointment_service.settings",
)

pytest.importorskip("django")

import django  # noqa: E402

django.setup()

from django.test import Client, override_settings  # noqa: E402


@pytest.fixture
def client():
    return Client(HTTP_HOST="localhost")


def test_home_page_has_navigation(client):
    response = client.get("/")

    assert response.status_code == 200
    page = response.content.decode()
    assert "Сервис записи к врачу" in page
    assert 'href="/doctors/"' in page
    assert 'href="/specialties/"' in page
    assert 'href="/patients/"' in page
    assert 'href="/appointments/"' in page
    assert "bootstrap@5.3.3" in page


def test_doctors_list_shows_domain_data(client):
    response = client.get("/doctors/")

    assert response.status_code == 200
    page = response.content.decode()
    assert "Смирнова Анна Сергеевна" in page
    assert "Петров Олег Викторович" in page
    assert 'href="/doctors/1/"' in page


def test_doctor_detail_uses_slot_check(client):
    response = client.get("/doctors/1/")

    assert response.status_code == 200
    page = response.content.decode()
    assert "Терапевт" in page
    assert "занят" in page
    assert "Иванов Иван Иванович" in page


def test_cancelled_slot_is_free_on_doctor_page(client):
    response = client.get("/doctors/2/")

    assert response.status_code == 200
    assert "свободен" in response.content.decode()


def test_missing_doctor_returns_404(client):
    response = client.get("/doctors/999/")

    assert response.status_code == 404
    assert "Врач не найден" in response.content.decode()


def test_specialties_and_detail(client):
    listing = client.get("/specialties/")
    detail = client.get("/specialties/Кардиолог/")

    assert listing.status_code == 200
    assert "Кардиолог" in listing.content.decode()
    assert detail.status_code == 200
    assert "Петров Олег Викторович" in detail.content.decode()


def test_unknown_specialty_returns_404(client):
    response = client.get("/specialties/Алхимик/")

    assert response.status_code == 404
    assert "Специальность не найдена" in response.content.decode()


def test_patients_come_from_appointments(client):
    listing = client.get("/patients/")
    detail = client.get("/patients/1/")

    assert listing.status_code == 200
    assert "Иванов Иван Иванович" in listing.content.decode()
    assert detail.status_code == 200
    page = detail.content.decode()
    assert "34" in page
    assert "совершеннолетний" in page


def test_missing_patient_returns_404(client):
    response = client.get("/patients/999/")

    assert response.status_code == 404
    assert "Пациент не найден" in response.content.decode()


def test_appointments_keep_cancelled_records(client):
    listing = client.get("/appointments/")
    active = client.get("/appointments/1/")
    cancelled = client.get("/appointments/3/")

    assert listing.status_code == 200
    assert "Сидоров Пётр Алексеевич" in listing.content.decode()
    assert active.status_code == 200
    active_page = active.content.decode()
    assert "Смирнова Анна Сергеевна" in active_page
    assert "Иванов Иван Иванович" in active_page
    assert cancelled.status_code == 200
    assert "отменена" in cancelled.content.decode()


def test_missing_appointment_returns_404(client):
    response = client.get("/appointments/999/")

    assert response.status_code == 404
    assert "Запись не найдена" in response.content.decode()


@override_settings(
    DEBUG=False,
    ALLOWED_HOSTS=["localhost", "127.0.0.1", "testserver"],
)
def test_unknown_url_uses_project_404_page(client):
    response = client.get("/nonexistent/")

    assert response.status_code == 404
    page = response.content.decode()
    assert "страница не найдена" in page
    assert 'href="/"' in page


def test_pages_use_templates_and_static(client):
    """Базовый шаблон подключает CSS, логотип и JavaScript."""
    response = client.get("/")

    assert response.status_code == 200
    page = response.content.decode()
    assert "homepage/css/style.css" in page
    assert "homepage/js/main.js" in page
    assert "homepage/img/logo.png" in page
    assert 'id="current-year"' in page
    assert "В справочнике 15 врачей" in page

    doctors = client.get("/doctors/")
    assert "doctor-card" in doctors.content.decode()

    appointments = client.get("/appointments/3/")
    assert "appointment-status" in appointments.content.decode()
