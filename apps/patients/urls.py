"""Маршруты пациентов."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.patients, name="patients"),
    path(
        "<int:patient_id>/",
        views.patient_detail,
        name="patient_detail",
    ),
]
