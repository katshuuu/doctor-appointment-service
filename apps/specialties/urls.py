"""Маршруты специальностей."""

from django.urls import path

from . import views

app_name = "specialties"

urlpatterns = [
    path("", views.specialties, name="list"),
    path(
        "<str:specialty_name>/",
        views.specialty_detail,
        name="detail",
    ),
]
