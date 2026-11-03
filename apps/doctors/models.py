"""Модель врача."""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


def build_doctor_slug(name, pk):
    """Собрать уникальный slug из транслитерации имени и id."""
    base_slug = slugify(unidecode(name)) or "doctor"
    return f"{base_slug}-{pk}"


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
    slug = models.SlugField(
        max_length=180,
        unique=True,
        editable=False,
        verbose_name="URL-идентификатор",
    )

    class Meta:
        ordering = ["pk"]
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Сформировать slug, если он ещё не задан."""
        if not self.slug:
            transliterated_name = unidecode(self.name)
            base_slug = slugify(transliterated_name) or "doctor"
            if self.pk:
                self.slug = f"{base_slug}-{self.pk}"
            else:
                super().save(*args, **kwargs)
                self.slug = f"{base_slug}-{self.pk}"
                super().save(update_fields=["slug"])
                return
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Вернуть адрес подробной страницы врача."""
        return reverse("doctors:detail", kwargs={"slug": self.slug})
