# Generated by Django 4.2.6 on 2024-01-27 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("purchases", "0003_remove_cashcheck_home_cashcheck_repair_object"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="position",
            options={
                "ordering": ("cash_check", "pk"),
                "verbose_name": "Позиция чека",
                "verbose_name_plural": "Позиции чека",
            },
        ),
        migrations.RemoveField(
            model_name="position",
            name="is_service",
        ),
        migrations.AddField(
            model_name="position",
            name="type",
            field=models.PositiveSmallIntegerField(
                choices=[(0, "Покупка"), (1, "Услуга"), (2, "Доставка")], default=0, verbose_name="Тип расходов"
            ),
        ),
    ]