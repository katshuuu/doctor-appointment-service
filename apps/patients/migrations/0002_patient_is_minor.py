from django.db import migrations, models
from django.db.models import Case, Value, When


class Migration(migrations.Migration):

    dependencies = [
        ("patients", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="patient",
            name="is_minor",
            field=models.GeneratedField(
                db_persist=True,
                expression=Case(
                    When(age__lt=18, then=Value(True)),
                    default=Value(False),
                    output_field=models.BooleanField(),
                ),
                output_field=models.BooleanField(),
                verbose_name="Несовершеннолетний",
            ),
        ),
    ]
