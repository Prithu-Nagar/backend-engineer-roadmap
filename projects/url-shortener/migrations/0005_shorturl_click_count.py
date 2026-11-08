"""Add click analytics to short URL records."""

from typing import ClassVar

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies: ClassVar[list] = [
        ("url_shortener", "0004_alter_shorturl_options"),
    ]

    operations: ClassVar[list] = [
        migrations.AddField(
            model_name="shorturl",
            name="click_count",
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
