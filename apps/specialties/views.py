"""Страницы сущности «Специальность»."""

from html import escape

from django.http import HttpResponse

from apps.homepage.views import page
from apps.loaders import load_domain, specialty_path
from doctors import filter_doctors_by_specialty
from entities.specialty import KNOWN_SPECIALTIES, is_known_specialty


def specialties(request):
    """Справочник специальностей и число врачей по каждой."""
    doctor_list, _appointments = load_domain()
    items = ""
    for specialty in KNOWN_SPECIALTIES:
        found = filter_doctors_by_specialty(doctor_list, specialty)
        items += (
            '<li class="list-group-item d-flex '
            'justify-content-between">'
            f'<a href="{specialty_path(specialty)}">'
            f"{escape(specialty)}</a>"
            f'<span class="badge bg-primary">{len(found)}</span>'
            "</li>"
        )
    content = f"""
    <h1>Специальности</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(
        page("Сервис записи к врачу – специальности", content),
    )


def specialty_detail(request, specialty_name):
    """Врачи выбранной специальности."""
    if not is_known_specialty(specialty_name):
        content = """
        <h1 class="text-danger">Специальность не найдена</h1>
        <a href="/specialties/" class="btn btn-outline-secondary">
            ← к списку специальностей
        </a>
        """
        return HttpResponse(
            page("Специальность не найдена", content),
            status=404,
        )
    doctor_list, _appointments = load_domain()
    found = filter_doctors_by_specialty(doctor_list, specialty_name)
    items = ""
    for doctor in found:
        items += (
            '<li class="list-group-item">'
            f'<a href="/doctors/{doctor.id}/">'
            f"{escape(doctor.name)}</a>"
            "</li>"
        )
    if not items:
        items = (
            '<li class="list-group-item">'
            "Врачей этой специальности пока нет"
            "</li>"
        )
    content = f"""
    <h1>{escape(specialty_name)}</h1>
    <ul class="list-group mb-3">{items}</ul>
    <a href="/specialties/" class="btn btn-outline-secondary">
        ← к списку специальностей
    </a>
    """
    return HttpResponse(
        page(specialty_name, content),
        status=200,
    )
