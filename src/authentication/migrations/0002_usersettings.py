# Generated by Django 4.0.1 on 2022-08-05 04:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homes', '0001_initial'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_home', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='settings', to='homes.home', verbose_name='Текущий дом')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Настройки пользователя',
                'verbose_name_plural': 'Настройки пользователя',
            },
        ),
    ]
