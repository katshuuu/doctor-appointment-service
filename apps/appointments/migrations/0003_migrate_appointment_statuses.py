from django.db import migrations


def migrate_appointment_statuses(apps, schema_editor):
    Appointment = apps.get_model("appointments", "Appointment")
    Appointment.objects.filter(is_cancelled=True).update(status="cancelled")
    Appointment.objects.filter(is_cancelled=False).update(status="active")


def reverse_appointment_statuses(apps, schema_editor):
    Appointment = apps.get_model("appointments", "Appointment")
    Appointment.objects.filter(status="cancelled").update(is_cancelled=True)
    Appointment.objects.exclude(status="cancelled").update(is_cancelled=False)


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0002_appointment_status"),
    ]

    operations = [
        migrations.RunPython(
            migrate_appointment_statuses,
            reverse_appointment_statuses,
        ),
    ]
