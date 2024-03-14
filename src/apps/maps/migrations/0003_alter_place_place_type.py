# Generated by Django 5.0.3 on 2024-03-14 10:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("maps", "0002_alter_floor_floor_map"),
    ]

    operations = [
        migrations.AlterField(
            model_name="place",
            name="place_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="maps.placetype",
            ),
        ),
    ]