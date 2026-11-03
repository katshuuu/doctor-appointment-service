from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0003_populate_doctor_slugs"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="slug",
            field=models.SlugField(
                editable=False,
                max_length=180,
                unique=True,
                verbose_name="URL-идентификатор",
            ),
        ),
    ]
