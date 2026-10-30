"""Модель записи на прием."""

from django.db import models


class Appointment(models.Model):
    """Запись пациента к врачу на дату и время."""

    id = models.BigAutoField(
        primary_key=True,
        verbose_name="Идентификатор",
    )
    doctor = models.ForeignKey(
        "doctors.Doctor",
        on_delete=models.PROTECT,
        related_name="appointments",
        verbose_name="Врач",
    )
    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.PROTECT,
        related_name="appointments",
        verbose_name="Пациент",
    )
    appointment_date = models.DateField(
        verbose_name="Дата приема",
    )
    appointment_time = models.TimeField(
        verbose_name="Время приема",
    )
    is_cancelled = models.BooleanField(
        default=False,
        verbose_name="Запись отменена",
    )

    class Meta:
        ordering = ["appointment_date", "appointment_time", "pk"]
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"

    def __str__(self):
        return (
            f"{self.patient} — {self.appointment_date} ({self.doctor})"
        )

    def cancel(self):
        """Пометить запись отменённой и сохранить только этот признак."""
        self.is_cancelled = True
        self.save(update_fields=["is_cancelled"])
