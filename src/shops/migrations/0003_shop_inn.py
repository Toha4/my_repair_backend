# Generated by Django 4.2.6 on 2024-02-25 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shops", "0002_alter_shop_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="shop",
            name="inn",
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name="ИНН"),
        ),
    ]
