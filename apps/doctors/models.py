"""Модель врача."""

from django.db import models


class Doctor(models.Model):
    """Врач и его специальность."""

    id = models.BigAutoField(
        primary_key=True,
        verbose_name="Идентификатор",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Имя",
    )
    specialty = models.ForeignKey(
        "specialties.Specialty",
        on_delete=models.PROTECT,
        related_name="doctors",
        verbose_name="Специальность",
    )

    class Meta:
        ordering = ["pk"]
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

    def __str__(self):
        return self.name
