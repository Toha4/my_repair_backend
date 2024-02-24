from django.db import models


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
