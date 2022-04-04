from django.db import models


class Shop(models.Model):
    user = models.ForeignKey(
        "authentication.CustomUser", verbose_name="Пользователь", on_delete=models.CASCADE, related_name="shops"
    )
    name = models.CharField(verbose_name="Наименование", max_length=32)
    link = models.CharField(verbose_name="Ссылка на сайт", max_length=128, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
        unique_together = ("name", "user")
        ordering = (
            "name",
            "-pk",
        )
