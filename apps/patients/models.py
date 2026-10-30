"""Модель пациента."""

from django.db import models

MINOR_AGE_LIMIT = 18


class Patient(models.Model):
    """Пациент, записанный на прием."""

    id = models.BigAutoField(
        primary_key=True,
        verbose_name="Идентификатор",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Имя",
    )
    age = models.PositiveIntegerField(
        verbose_name="Возраст",
    )

    class Meta:
        ordering = ["pk"]
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __str__(self):
        return self.name

    @property
    def is_minor(self):
        """Пациент младше 18 лет."""
        return self.age < MINOR_AGE_LIMIT
