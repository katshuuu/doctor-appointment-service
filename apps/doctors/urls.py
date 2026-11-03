"""Маршруты врачей."""

from django.urls import path

from . import views

app_name = "doctors"

urlpatterns = [
    path("", views.doctors, name="list"),
    path("available/", views.available_doctors, name="available"),
    path("<slug:slug>/", views.doctor_detail, name="detail"),
]
