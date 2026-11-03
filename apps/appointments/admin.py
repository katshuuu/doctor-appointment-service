"""Регистрация записи на прием в административном интерфейсе."""

from django.contrib import admin

from .models import Appointment


class DoctorAppointmentInline(admin.TabularInline):
    """Записи врача на странице редактирования врача."""

    model = Appointment
    fk_name = "doctor"
    fields = (
        "patient",
        "appointment_date",
        "appointment_time",
        "status",
    )
    extra = 0
    can_delete = False
    show_change_link = True


class PatientAppointmentInline(admin.TabularInline):
    """Записи пациента на странице редактирования пациента."""

    model = Appointment
    fk_name = "patient"
    fields = (
        "doctor",
        "appointment_date",
        "appointment_time",
        "status",
    )
    extra = 0
    can_delete = False
    show_change_link = True


@admin.action(description="Отменить выбранные записи")
def cancel_selected(modeladmin, request, queryset):
    """Отметить выбранные записи отменёнными через метод модели."""
    for appointment in queryset.active():
        appointment.cancel()


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "appointment_date",
        "appointment_time",
        "doctor",
        "patient",
        "status",
    )
    list_display_links = ("id",)
    list_filter = ("status", "appointment_date", "doctor")
    search_fields = ("doctor__name", "patient__name")
    ordering = ("appointment_date", "appointment_time", "pk")
    readonly_fields = ("id",)
    actions = (cancel_selected,)
    list_select_related = ("doctor", "patient")
