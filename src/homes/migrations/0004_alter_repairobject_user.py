# Generated by Django 4.0 on 2023-10-31 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_rename_current_object_usersettings_current_repair_object'),
        ('homes', '0003_delete_home'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repairobject',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repair_objects', to='authentication.customuser', verbose_name='Пользователь'),
        ),
    ]
