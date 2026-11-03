from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="slug",
            field=models.SlugField(
                blank=True,
                editable=False,
                max_length=180,
                verbose_name="URL-идентификатор",
            ),
        ),
    ]
