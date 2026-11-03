"""Корневая маршрутизация Django-проекта."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Сервис записи к врачу"
admin.site.site_title = "Администрирование"
admin.site.index_title = "Управление данными"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.homepage.urls")),
    path("doctors/", include("apps.doctors.urls")),
    path("specialties/", include("apps.specialties.urls")),
    path("patients/", include("apps.patients.urls")),
    path("appointments/", include("apps.appointments.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        *urlpatterns,
    ]

handler404 = "apps.homepage.views.page_not_found"
