from django.db import models


class TimestampModel(models.Model):
    created = models.DateTimeField(verbose_name="Создано", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Обновлено", auto_now=True)

    class Meta:
        abstract = True
