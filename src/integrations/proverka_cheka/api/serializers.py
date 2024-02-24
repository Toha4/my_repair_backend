from rest_framework import serializers

from app.serializers import CurrentUserDefault
from integrations.proverka_cheka.models import ProverkaChekaIntegration


class ProverkaChekaIntegrationViewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = ProverkaChekaIntegration
        fields = (
            "user",
            "is_enabled",
            "api_key",
        )
