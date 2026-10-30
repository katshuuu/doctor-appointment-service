"""Модель специальности."""

from django.db import models


class Specialty(models.Model):
    """Справочник специальностей врачей."""

    id = models.BigAutoField(
        primary_key=True,
        verbose_name="Идентификатор",
    )
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"

    def __str__(self):
        return self.name
