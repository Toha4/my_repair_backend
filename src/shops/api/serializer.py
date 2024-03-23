from rest_framework import serializers

from app.serializers import CurrentUserDefault

from ..models import Shop


class ShopSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Shop
        fields = (
            "pk",
            "user",
            "name",
            "link",
            "inn",
            "description",
        )
