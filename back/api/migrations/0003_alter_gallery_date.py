# Generated by Django 4.1.2 on 2023-07-01 09:55

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_year_alter_file_gallery_promo_gallery_year_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gallery",
            name="date",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
