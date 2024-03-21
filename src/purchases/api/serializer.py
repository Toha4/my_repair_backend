from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from app.serializers import SERIALIZER_DATE_PARAMS
from app.serializers import CurrentUserDefault
from homes.models import RepairObject

from ..models import CashCheck
from ..models import Position


class PositionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Position
        fields = (
            "pk",
            "user",
            "name",
            "room",
            "category",
            "link",
            "note",
            "price",
            "quantity",
            "type",
        )


class PositionFullSerializer(PositionSerializer):
    room_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta(PositionSerializer.Meta):
        fields = PositionSerializer.Meta.fields + ("room_name", "category_name")

    def get_room_name(self, obj):
        if obj.cash_check.repair_object.type_object == RepairObject.LAND and obj.room.building:
            return f"{obj.room.building.name} - {obj.room.name}"
        return obj.room.name

    def get_category_name(self, obj):
        if obj.category:
            return obj.category.name
        return ""


class PositionUpdateSerializer(PositionFullSerializer):
    check_date = serializers.SerializerMethodField()
    check_number = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()

    class Meta(PositionSerializer.Meta):
        fields = PositionSerializer.Meta.fields + ("check_date", "check_number", "shop_name")

    def get_check_date(self, obj: Position):
        return obj.cash_check.date.strftime("%d.%m.%Y")

    def get_check_number(self, obj: Position):
        # TODO: Пока номер чека это id, в дальнейшем пранирую переделать
        return obj.cash_check.id

    def get_shop_name(self, obj):
        if obj.cash_check.shop:
            return obj.cash_check.shop.name
        return None


class PositionListSerializer(PositionFullSerializer):
    cash_check_id = serializers.IntegerField(source="cash_check.id", read_only=True)
    shop = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()
    cash_check_date = serializers.SerializerMethodField()
    room_name = serializers.SerializerMethodField()

    class Meta(PositionFullSerializer.Meta):
        fields = PositionFullSerializer.Meta.fields + ("cash_check_id", "shop", "shop_name", "cash_check_date")

    def get_shop(self, obj):
        if obj.cash_check.shop:
            return obj.cash_check.shop.id
        return None

    def get_shop_name(self, obj):
        if obj.cash_check.shop:
            return obj.cash_check.shop.name
        return None

    def get_cash_check_date(self, obj):
        if obj.cash_check.date:
            return obj.cash_check.date.strftime("%d.%m.%Y")
        return None


class PositionNestedSerializer(PositionSerializer):
    class Meta(PositionSerializer.Meta):
        ordering = ["-pk"]


class CashCheckSerializer(WritableNestedModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    date = serializers.DateField(**SERIALIZER_DATE_PARAMS)
    positions = PositionNestedSerializer(many=True)

    class Meta:
        model = CashCheck
        fields = (
            "pk",
            "user",
            "date",
            "shop",
            "receipt_scanning",
            "positions",
        )

    def validate(self, data):
        errors = {}
        positions = data.get("positions")

        if self.instance and self.instance.user:
            user = self.instance.user
        else:
            user = data.get("user")

        error_positions = []
        for position in positions:
            error_position = {}

            room = position.get("room")
            if room.user != user:
                error_position["room"] = "Комната не найдена."

            category = position.get("category")
            if category.user != user:
                error_position["category"] = "Категория не найдена."

            if error_position:
                error_positions.append(error_position)

        if error_positions:
            errors["positions"] = error_positions

        if errors:
            raise serializers.ValidationError(errors)

        return data


class CashCheckFullSerializer(CashCheckSerializer):
    positions = PositionFullSerializer(many=True)
    repair_object_name = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()

    class Meta(CashCheckSerializer.Meta):
        fields = CashCheckSerializer.Meta.fields + ("repair_object_name", "shop_name")

    def get_repair_object_name(self, obj):
        if obj.repair_object:
            return obj.repair_object.name
        return ""

    def get_shop_name(self, obj):
        if obj.shop:
            return obj.shop.name
        return ""
