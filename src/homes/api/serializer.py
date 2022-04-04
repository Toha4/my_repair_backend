from rest_framework import serializers

from app.serializers import CurrentUserDefault

from ..models import Home
from ..models import Room


class HomeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Home
        fields = (
            "pk",
            "user",
            "name",
            "type_home",
            "square",
        )


class RoomSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Room
        fields = (
            "pk",
            "user",
            "home",
            "name",
            "square",
            "date_begin",
            "date_end",
        )

    def validate(self, data):
        user = data.get("user")
        home = data.get("home")

        if home.user != user:
            raise serializers.ValidationError({"home": ("Дом принадлежит другому пользователю.")})

        return data
