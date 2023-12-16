from rest_framework import serializers

from app.serializers import SERIALIZER_DATE_PARAMS
from app.serializers import CurrentUserDefault

from ..models import Building
from ..models import RepairObject
from ..models import Room


class RepairObjectSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    type_object_name = serializers.ReadOnlyField(read_only=True)

    class Meta:
        model = RepairObject
        fields = (
            "pk",
            "user",
            "name",
            "type_object",
            "type_object_name",
            "square",
        )

    def validate_type_object(self, value):
        # Тип объекта нельзя изменить
        if self.instance and self.instance.type_object != value:
            raise serializers.ValidationError("Type object cannot be changed")

        return value


class BuildingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    date_begin = serializers.DateField(**SERIALIZER_DATE_PARAMS, required=False, allow_null=True)
    date_end = serializers.DateField(**SERIALIZER_DATE_PARAMS, required=False, allow_null=True)

    class Meta:
        model = Building
        fields = (
            "pk",
            "user",
            "name",
            "square",
            "date_begin",
            "date_end",
        )


class RoomSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    date_begin = serializers.DateField(**SERIALIZER_DATE_PARAMS, required=False, allow_null=True)
    date_end = serializers.DateField(**SERIALIZER_DATE_PARAMS, required=False, allow_null=True)
    building_name = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "pk",
            "user",
            "building",
            "building_name",
            "name",
            "square",
            "date_begin",
            "date_end",
        )

    def get_building_name(self, obj):
        if obj.building:
            return obj.building.name
        return None
