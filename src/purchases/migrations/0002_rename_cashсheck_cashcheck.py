# Generated by Django 4.0.1 on 2023-10-21 14:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homes', '0001_initial'),
        ('shops', '0002_alter_shop_name'),
        ('purchases', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CashСheck',
            new_name='CashCheck',
        ),
    ]
