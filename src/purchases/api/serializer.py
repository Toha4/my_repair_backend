from django.db.transaction import atomic

from rest_framework import serializers

from app.serializers import SERIALIZER_DATE_PARAMS
from app.serializers import CurrentUserDefault

from ..models import CashСheck
from ..models import Position


class PositionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    cahs_check = serializers.PrimaryKeyRelatedField(queryset=CashСheck.objects.all(), write_only=True, required=False)

    class Meta:
        model = Position
        fields = (
            "pk",
            "user",
            "cahs_check",
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
        if obj.room:
            return obj.room.name
        return ""

    def get_category_name(self, obj):
        if obj.category:
            return obj.category.name
        return ""


class PositionListSerializer(PositionFullSerializer):
    cahs_check = serializers.PrimaryKeyRelatedField(read_only=True)
    shop = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta(PositionSerializer.Meta):
        fields = PositionSerializer.Meta.fields + ("shop", "shop_name", "date")

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


class CashСheckSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    date = serializers.DateField(**SERIALIZER_DATE_PARAMS)
    positions = PositionSerializer(many=True)

    class Meta:
        model = CashСheck
        fields = (
            "pk",
            "user",
            "home",
            "date",
            "shop",
            "positions",
        )

    def validate(self, data):
        errors = {}
        positions = data.get("positions")
        home = data.get("home")

        if self.instance and self.instance.user:
            user = self.instance.user
        else:
            user = data.get("user")

        if home.user != user:
            errors["home"] = "Дом принадлежит другому пользователю."

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


class CashСheckFullSerializer(CashСheckSerializer):
    positions = PositionFullSerializer(many=True)
    home_name = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()

    class Meta(CashСheckSerializer.Meta):
        fields = CashСheckSerializer.Meta.fields + ("home_name", "shop_name")

    def get_home_name(self, obj):
        if obj.home:
            return obj.home.name
        return ""

    def get_shop_name(self, obj):
        if obj.shop:
            return obj.shop.name
        return ""
