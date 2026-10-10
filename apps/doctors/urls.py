"""Маршруты врачей."""

from django.urls import path

from . import views

app_name = "doctors"

urlpatterns = [
    path("", views.doctors, name="list"),
    path("<int:doctor_id>/", views.doctor_detail, name="detail"),
]
