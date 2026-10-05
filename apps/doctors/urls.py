"""Маршруты врачей."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.doctors, name="doctors"),
    path("<int:doctor_id>/", views.doctor_detail, name="doctor_detail"),
]
