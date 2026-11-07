"""
Align URL destination length with the API validation limit.
"""

from typing import ClassVar

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies: ClassVar[list] = [
        ("url_shortener", "0002_shorturl_owner"),
    ]

    operations: ClassVar[list] = [
        migrations.AlterField(
            model_name="shorturl",
            name="original_url",
            field=models.URLField(max_length=2048),
        ),
    ]
