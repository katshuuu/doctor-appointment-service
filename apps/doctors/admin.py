"""Регистрация врача в административном интерфейсе."""

from django.contrib import admin

from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "specialty")
    list_filter = ("specialty",)
    search_fields = ("name", "specialty__name")
    ordering = ("pk",)
