"""Страницы сущности «Специальность». Данные читаются через Django ORM."""

from django.db.models import Count
from django.shortcuts import render

from apps.doctors.models import Doctor
from apps.specialties.models import Specialty


def specialties(request):
    """Справочник специальностей и число врачей по каждой."""
    context = {
        "specialties": Specialty.objects.annotate(
            doctor_count=Count("doctors"),
        ).order_by("pk"),
    }
    return render(
        request,
        "specialties/specialty_list.html",
        context,
    )


def specialty_detail(request, specialty_name):
    """Врачи выбранной специальности."""
    try:
        specialty = Specialty.objects.get(name=specialty_name)
    except Specialty.DoesNotExist:
        return render(
            request,
            "specialties/specialty_detail.html",
            {"specialty": None},
            status=404,
        )
    doctors = Doctor.objects.filter(
        specialty__name=specialty.name,
    ).select_related("specialty").order_by("name")
    context = {
        "specialty": specialty,
        "doctors": doctors,
    }
    return render(
        request,
        "specialties/specialty_detail.html",
        context,
    )
