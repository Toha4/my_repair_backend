from django.db import migrations, models


def populate_sequence_number(apps, schema_editor):
    CashCheck = apps.get_model('purchases', 'CashCheck')
    User = apps.get_model('authentication', 'CustomUser')
    for user in User.objects.all():
        # Чеки пользователя, отсортированные по дате (и id для определённости)
        checks = CashCheck.objects.filter(user=user).order_by('date', 'id')
        seq = 1
        for check in checks:
            check.sequence_number = seq
            check.save(update_fields=['sequence_number'])
            seq += 1


def reverse_populate(apps, schema_editor):
    # При откате можно сбросить sequence_number в 0 (или оставить как есть)
    CashCheck = apps.get_model('purchases', 'CashCheck')
    CashCheck.objects.update(sequence_number=0)


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0009_cashcheck_sequence_number_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_sequence_number, reverse_populate),
        migrations.AddConstraint(
            model_name="cashcheck",
            constraint=models.UniqueConstraint(fields=("user", "sequence_number"), name="unique_user_sequence"),
        ),
    ]