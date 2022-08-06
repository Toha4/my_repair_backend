from rest_framework import serializers

from app.serializers import SERIALIZER_DATE_PARAMS
from app.serializers import CurrentUserDefault

from ..models import Home
from ..models import Room


class HomeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    type_home_name = serializers.ReadOnlyField(read_only=True)

    class Meta:
        model = Home
        fields = (
            "pk",
            "user",
            "name",
            "type_home",
            "type_home_name",
            "square",
        )


class RoomSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    date_begin = serializers.DateField(**SERIALIZER_DATE_PARAMS, required=False, allow_null=True)
    date_end = serializers.DateField(**SERIALIZER_DATE_PARAMS, required=False, allow_null=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "user",
            "name",
            "square",
            "date_begin",
            "date_end",
        )
