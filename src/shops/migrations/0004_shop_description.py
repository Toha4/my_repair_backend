# Generated by Django 4.2.6 on 2024-03-23 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shops", "0003_shop_inn"),
    ]

    operations = [
        migrations.AddField(
            model_name="shop",
            name="description",
            field=models.TextField(blank=True, verbose_name="Описание"),
        ),
    ]
