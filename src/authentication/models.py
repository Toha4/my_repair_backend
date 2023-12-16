from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class UserSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="settings")
    current_repair_object = models.ForeignKey(
        "homes.RepairObject",
        verbose_name="Текущий объект ремонта",
        on_delete=models.PROTECT,
        related_name="settings",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        verbose_name = "Настройки пользователя"
        verbose_name_plural = "Настройки пользователя"
