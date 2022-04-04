from django.db import models


class Category(models.Model):
    user = models.ForeignKey(
        "authentication.CustomUser", verbose_name="Пользователь", on_delete=models.CASCADE, related_name="categories"
    )
    name = models.CharField(verbose_name="Наименование", max_length=32)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ("name", "user")
        ordering = ("name", "-pk")
