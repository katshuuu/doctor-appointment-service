"""Регистрация пациента в административном интерфейсе."""

from django.contrib import admin

from apps.appointments.admin import PatientAppointmentInline

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age", "is_minor")
    list_display_links = ("name",)
    list_filter = ("is_minor",)
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("id", "is_minor")
    inlines = (PatientAppointmentInline,)
    list_per_page = 20
