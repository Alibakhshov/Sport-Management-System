# Generated by Django 4.2 on 2023-05-04 05:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ucasports", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="competition",
            name="location",
            field=models.CharField(default="Sport Bubble", max_length=200),
        ),
    ]
