# Generated by Django 2.1.5 on 2023-01-15 11:08

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rango", "0004_auto_20220921_1652"),
    ]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="last_visit",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 1, 15, 14, 8, 5, 626349)
            ),
        ),
    ]
