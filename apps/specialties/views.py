"""Страницы сущности «Специальность»."""

from django.shortcuts import render

from apps.loaders import load_domain
from doctors import filter_doctors_by_specialty
from entities.specialty import KNOWN_SPECIALTIES, is_known_specialty


def specialties(request):
    """Справочник специальностей и число врачей по каждой."""
    doctor_list, _appointments = load_domain()
    rows = []
    for name in KNOWN_SPECIALTIES:
        found = filter_doctors_by_specialty(doctor_list, name)
        rows.append({
            "name": name,
            "doctors": found,
        })
    context = {
        "specialties": rows,
    }
    return render(
        request,
        "specialties/specialty_list.html",
        context,
    )


def specialty_detail(request, specialty_name):
    """Врачи выбранной специальности."""
    if not is_known_specialty(specialty_name):
        return render(
            request,
            "specialties/specialty_detail.html",
            {"specialty": None},
            status=404,
        )
    doctor_list, _appointments = load_domain()
    found = filter_doctors_by_specialty(
        doctor_list,
        specialty_name,
    )
    context = {
        "specialty": specialty_name,
        "doctors": found,
    }
    return render(
        request,
        "specialties/specialty_detail.html",
        context,
    )
