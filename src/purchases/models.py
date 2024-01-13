from django.db import models


class CashCheck(models.Model):
    user = models.ForeignKey(
        "authentication.CustomUser", verbose_name="Пользователь", on_delete=models.CASCADE, related_name="cash_checks"
    )
    repair_object = models.ForeignKey("homes.RepairObject", verbose_name="Объект ремонта", on_delete=models.PROTECT, related_name="cash_checks")
    date = models.DateField("Дата")
    shop = models.ForeignKey(
        "shops.Shop", verbose_name="Магазин", on_delete=models.PROTECT, related_name="cash_checks"
    )

    def __str__(self) -> str:
        return f"{self.shop} {self.date}"

    class Meta:
        verbose_name = "Чек"
        verbose_name_plural = "Чеки"
        ordering = ("-date", "-pk")

    def save(self, *args, **kwargs):
        self.repair_object = self.user.settings.current_repair_object
        super(CashCheck, self).save(*args, **kwargs)


class Position(models.Model):
    user = models.ForeignKey(
        "authentication.CustomUser",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="cash_checks_positions",
    )
    cash_check = models.ForeignKey(CashCheck, verbose_name="Чек", on_delete=models.CASCADE, related_name="positions")
    name = models.CharField(verbose_name="Наименование", max_length=128)
    room = models.ForeignKey(
        "homes.Room", verbose_name="Комната", on_delete=models.PROTECT, related_name="cash_checks_positions"
    )
    category = models.ForeignKey(
        "core.Category", verbose_name="Категория", on_delete=models.PROTECT, related_name="cash_checks_positions"
    )
    link = models.TextField(verbose_name="Ссылка на сайт", blank=True)
    note = models.TextField(verbose_name="Примечание", blank=True)
    price = models.DecimalField(verbose_name="Цена", max_digits=18, decimal_places=2)
    quantity = models.IntegerField(verbose_name="Количество")
    is_service = models.BooleanField(verbose_name="Услуга", default=False)

    def __str__(self) -> str:
        return f"{self.name} X {self.quantity} {self.price} руб."

    class Meta:
        verbose_name = "Позиция чека"
        verbose_name_plural = "Позиции чека"
        unique_together = ("cash_check", "name")
        ordering = ("cash_check", "pk")
