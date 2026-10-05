"""Маршруты специальностей."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.specialties, name="specialties"),
    path(
        "<str:specialty_name>/",
        views.specialty_detail,
        name="specialty_detail",
    ),
]
