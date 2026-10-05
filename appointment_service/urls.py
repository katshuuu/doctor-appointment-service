"""Корневая маршрутизация Django-проекта."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.homepage.urls")),
    path("doctors/", include("apps.doctors.urls")),
    path("specialties/", include("apps.specialties.urls")),
    path("patients/", include("apps.patients.urls")),
    path("appointments/", include("apps.appointments.urls")),
]

handler404 = "apps.homepage.views.page_not_found"
