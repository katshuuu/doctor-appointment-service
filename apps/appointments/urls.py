"""Маршруты записей на прием."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.appointments, name="appointments"),
    path(
        "<int:appointment_id>/",
        views.appointment_detail,
        name="appointment_detail",
    ),
]
