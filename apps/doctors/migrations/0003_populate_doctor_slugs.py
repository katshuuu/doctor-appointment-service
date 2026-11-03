from django.db import migrations
from django.utils.text import slugify
from unidecode import unidecode


def populate_doctor_slugs(apps, schema_editor):
    Doctor = apps.get_model("doctors", "Doctor")
    for doctor in Doctor.objects.all():
        base_slug = slugify(unidecode(doctor.name)) or "doctor"
        doctor.slug = f"{base_slug}-{doctor.pk}"
        doctor.save(update_fields=["slug"])


def unpopulate_doctor_slugs(apps, schema_editor):
    Doctor = apps.get_model("doctors", "Doctor")
    Doctor.objects.update(slug="")


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0002_doctor_slug"),
    ]

    operations = [
        migrations.RunPython(
            populate_doctor_slugs,
            unpopulate_doctor_slugs,
        ),
    ]
