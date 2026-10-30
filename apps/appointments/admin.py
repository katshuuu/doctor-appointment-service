"""Регистрация записи на прием в административном интерфейсе."""

from django.contrib import admin

from .models import Appointment


@admin.action(description="Отменить выбранные записи")
def cancel_selected(modeladmin, request, queryset):
    """Отметить выбранные записи отменёнными через метод модели."""
    for appointment in queryset.filter(is_cancelled=False):
        appointment.cancel()


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "appointment_date",
        "appointment_time",
        "doctor",
        "patient",
        "is_cancelled",
    )
    list_filter = ("is_cancelled", "appointment_date", "doctor")
    search_fields = ("doctor__name", "patient__name")
    ordering = ("appointment_date", "appointment_time", "pk")
    actions = (cancel_selected,)
