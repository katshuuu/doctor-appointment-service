"""Модель записи на прием."""

from django.db import models


class AppointmentQuerySet(models.QuerySet):
    """Набор запросов для работы с записями на прием."""

    def active(self):
        """Вернуть только активные записи."""
        return self.filter(status=self.model.Status.ACTIVE)

    def cancelled(self):
        """Вернуть только отменённые записи."""
        return self.filter(status=self.model.Status.CANCELLED)

    def completed(self):
        """Вернуть только завершённые записи."""
        return self.filter(status=self.model.Status.COMPLETED)

    def for_date(self, selected_date):
        """Вернуть записи за указанную дату."""
        return self.filter(appointment_date=selected_date)


class AppointmentManager(
    models.Manager.from_queryset(AppointmentQuerySet),
):
    """Менеджер модели Appointment с дополнительными методами."""


class Appointment(models.Model):
    """Запись пациента к врачу на дату и время."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Активно"
        CANCELLED = "cancelled", "Отменено"
        COMPLETED = "completed", "Завершено"

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
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Статус записи",
    )
    objects = AppointmentManager()

    class Meta:
        ordering = ["appointment_date", "appointment_time", "pk"]
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"

    def __str__(self):
        return (
            f"{self.patient} — {self.appointment_date} ({self.doctor})"
        )

    def cancel(self):
        """Пометить запись отменённой и сохранить только статус."""
        self.status = self.Status.CANCELLED
        self.save(update_fields=["status"])
