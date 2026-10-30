"""Регистрация пациента в административном интерфейсе."""

from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age")
    search_fields = ("name",)
    ordering = ("pk",)
