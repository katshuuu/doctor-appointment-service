"""Регистрация специальности в административном интерфейсе."""

from django.contrib import admin

from .models import Specialty


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("id",)
