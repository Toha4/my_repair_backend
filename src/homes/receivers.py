from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication.models import UserSettings
from homes.models import Home


@receiver(post_save, sender=Home)
def set_active_home(sender, instance, created, **kwargs):
    if created:
        user_settings = UserSettings.objects.filter(user=instance.user).first()
        if not user_settings:
            user_settings = UserSettings(user=instance.user)

        if user_settings.current_home is None:
            user_settings.current_home = instance
            user_settings.save()
