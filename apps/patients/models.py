"""Модель пациента."""

from django.db import models
from django.db.models import Case, Value, When

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
    is_minor = models.GeneratedField(
        expression=Case(
            When(age__lt=MINOR_AGE_LIMIT, then=Value(True)),
            default=Value(False),
            output_field=models.BooleanField(),
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name="Несовершеннолетний",
    )

    class Meta:
        ordering = ["pk"]
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __str__(self):
        return self.name
