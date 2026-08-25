"""
Day 25 migration: associate short URLs with Django users.
"""

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("url_shortener", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shorturl",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.CASCADE,
                related_name="short_urls",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
