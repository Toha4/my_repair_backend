from django.db import models

from app.models import TimestampModel


class ProverkaChekaIntegration(models.Model):
    user = models.OneToOneField(
        "authentication.CustomUser", verbose_name="Пользователь", on_delete=models.CASCADE, primary_key=True
    )
    is_enabled = models.BooleanField(verbose_name="Интеграция включена", default=False)
    api_key = models.CharField(verbose_name="Токен доступа к API", max_length=32, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user}"

    class Meta:
        verbose_name = 'Интеграция "Проверка чека"'
        verbose_name_plural = 'Интеграции "Проверка чека"'


class ReceiptScanning(TimestampModel):
    user = models.ForeignKey(
        "authentication.CustomUser",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="receipt_scanning",
    )
    qr_raw = models.TextField(verbose_name="Строка сырых данных QR-кода", unique=True)
    organization = models.CharField(verbose_name="Организация", max_length=256)
    retail_place_addres = models.CharField(verbose_name="Адрес", max_length=256, null=True)
    organization_inn = models.CharField(verbose_name="ИНН организации", max_length=12)
    date = models.DateTimeField(verbose_name="Дата и время", null=True)
    request_number = models.IntegerField(verbose_name="Чек: №", null=True)
    operator = models.CharField(verbose_name="Кассир", max_length=256, null=True)
    total_sum = models.DecimalField(verbose_name="Итого", max_digits=18, decimal_places=2)
    html = models.TextField(verbose_name="html представление чека")

    def __str__(self) -> str:
        return f"{self.date} - {self.organization}"

    class Meta:
        verbose_name = "Сканированный чек"
        verbose_name_plural = "Сканированные чеки"
        ordering = ("-date",)


class ReceiptItem(models.Model):
    receipt = models.ForeignKey(ReceiptScanning, verbose_name="Чек", on_delete=models.CASCADE, related_name="items")
    name = models.CharField(verbose_name="Название товара/услуги", max_length=256)
    price = models.DecimalField(verbose_name="Цена", max_digits=18, decimal_places=2)
    quantity = models.DecimalField(verbose_name="Количество", max_digits=18, decimal_places=3)
    sum = models.DecimalField(verbose_name="Сумма", max_digits=18, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.name} x {self.quantity}"

    class Meta:
        verbose_name = "Позиция в чеке"
        verbose_name_plural = "Позиции в чеке"
