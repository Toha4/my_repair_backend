from django.apps import AppConfig


class GetReceiptsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "integrations.get_receipts"
    verbose_name = "Интеграция для получения данных чеков"
