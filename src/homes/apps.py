from django.apps import AppConfig


class HomesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "homes"
    verbose_name = "Дом"
    verbose_name_plural = "Дома"

    def ready(self):
        from homes import receivers     # noqa