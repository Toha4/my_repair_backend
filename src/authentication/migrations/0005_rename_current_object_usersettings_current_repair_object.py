# Generated by Django 4.0 on 2023-10-31 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_usersettings_current_object'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usersettings',
            old_name='current_object',
            new_name='current_repair_object',
        ),
    ]
