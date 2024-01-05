from django.db.transaction import atomic

from rest_framework import serializers

from app.serializers import SERIALIZER_DATE_PARAMS
from app.serializers import CurrentUserDefault
from homes.models import RepairObject

from ..models import CashCheck
from ..models import Position


class PositionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    cash_check = serializers.PrimaryKeyRelatedField(queryset=CashCheck.objects.all(), write_only=True, required=False)

    class Meta:
        model = Position
        fields = (
            "pk",
            "user",
            "cash_check",
            "name",
            "room",
            "category",
            "link",
            "note",
            "price",
            "quantity",
            "is_service",
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


class PositionListSerializer(PositionFullSerializer):
    cash_check = serializers.PrimaryKeyRelatedField(queryset=CashCheck.objects.all())
    shop = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    room_name = serializers.SerializerMethodField()

    class Meta(PositionFullSerializer.Meta):
        fields = PositionFullSerializer.Meta.fields + ("shop", "shop_name", "date")

    def get_shop(self, obj):
        if obj.cash_check.shop:
            return obj.cash_check.shop.id
        return None

    def get_shop_name(self, obj):
        if obj.cash_check.shop:
            return obj.cash_check.shop.name
        return None

    def get_date(self, obj):
        if obj.cash_check.date:
            return obj.cash_check.date.strftime("%d.%m.%Y")
        return None


class CashCheckSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    date = serializers.DateField(**SERIALIZER_DATE_PARAMS)
    positions = PositionSerializer(many=True)

    class Meta:
        model = CashCheck
        fields = (
            "pk",
            "user",
            "repair_object",
            "date",
            "shop",
            "positions",
        )

    def validate(self, data):
        errors = {}
        positions = data.get("positions")
        repair_object = data.get("repair_object")

        if self.instance and self.instance.user:
            user = self.instance.user
        else:
            user = data.get("user")

        if repair_object.user != user:
            errors["repair_object"] = "Объект ремонта принадлежит другому пользователю."

        error_positions = []
        for position in positions:
            error_position = {}

            room = position.get("room")
            if room.user != user:
                error_position["room"] = "Комната принадлежит другому пользователю."

            category = position.get("category")
            if category.user != user:
                error_position["category"] = "Категория принадлежит другому пользователю."

            if error_position:
                error_positions.append(error_position)

        if error_positions:
            errors["positions"] = error_positions

        if errors:
            raise serializers.ValidationError(errors)

        return data

    @atomic
    def create(self, validated_data):
        positions = validated_data.pop("positions")
        cash_check = self.Meta.model.objects.create(**validated_data)
        for position in positions:
            cash_check.positions.create(**position)

        return cash_check

    @atomic
    def update(self, instance, validated_data):
        positions = validated_data.pop("positions")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        instance.positions.all().delete()
        for position in positions:
            position["user"] = instance.user
            instance.positions.create(**position)

        return instance


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
