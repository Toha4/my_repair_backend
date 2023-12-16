from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication.models import UserSettings
from homes.models import RepairObject


@receiver(post_save, sender=RepairObject)
def set_active_repair_object(sender, instance, created, **kwargs):
    if created:
        user_settings = UserSettings.objects.filter(user=instance.user).first()
        if not user_settings:
            user_settings = UserSettings(user=instance.user)

        if user_settings.current_repair_object is None:
            user_settings.current_repair_object = instance
            user_settings.save()
