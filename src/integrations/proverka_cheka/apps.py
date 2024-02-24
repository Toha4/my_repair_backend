from django.apps import AppConfig


class ProverkaChekaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "integrations.proverka_cheka"
    verbose_name = "Интеграция для получения данных чеков"
