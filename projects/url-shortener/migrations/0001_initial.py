"""
Initial Django migration for the URL Shortener project.
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ShortURL",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("short_code", models.CharField(max_length=32, unique=True)),
                ("original_url", models.URLField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expires_at", models.DateTimeField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
