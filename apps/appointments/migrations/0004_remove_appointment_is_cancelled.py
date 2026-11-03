from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0003_migrate_appointment_statuses"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="appointment",
            name="is_cancelled",
        ),
    ]
