"""Регистрация врача в административном интерфейсе."""

from django.contrib import admin
from django.utils.html import format_html

from apps.appointments.admin import DoctorAppointmentInline

from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "specialty", "slug", "site_link")
    list_display_links = ("name",)
    list_filter = ("specialty",)
    search_fields = ("name", "specialty__name", "slug")
    ordering = ("name",)
    readonly_fields = ("id", "slug")
    inlines = (DoctorAppointmentInline,)
    list_select_related = ("specialty",)
    view_on_site = True
    list_per_page = 20

    @admin.display(description="Страница на сайте")
    def site_link(self, obj):
        """Ссылка на публичную карточку врача."""
        if not obj.slug:
            return "—"
        return format_html(
            '<a href="{}" target="_blank">Открыть</a>',
            obj.get_absolute_url(),
        )
