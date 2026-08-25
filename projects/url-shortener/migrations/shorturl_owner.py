"""
Add authenticated ownership to ShortURL records.
"""

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("url_shortener", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shorturl",
            name="owner",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="short_urls",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
