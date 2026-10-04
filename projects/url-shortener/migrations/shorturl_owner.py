"""
Add authenticated ownership to ShortURL records.
"""

from typing import ClassVar

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies: ClassVar[list] = [
        ("url_shortener", "0001_initial"),
    ]

    operations: ClassVar[list] = [
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
