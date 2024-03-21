from django.db.transaction import atomic

from rest_framework import serializers

from app.serializers import SERIALIZER_DATETIME_PARAMS
from app.serializers import CurrentUserDefault
from integrations.proverka_cheka.models import ProverkaChekaIntegration
from integrations.proverka_cheka.models import ReceiptItem
from integrations.proverka_cheka.models import ReceiptScanning
from shops.models import Shop


class ProverkaChekaIntegrationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = ProverkaChekaIntegration
        fields = (
            "user",
            "is_enabled",
            "api_key",
        )


class ReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptItem
        fields = (
            "name",
            "price",
            "quantity",
            "sum",
        )


class ReceiptScanningDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    created = serializers.DateTimeField(**SERIALIZER_DATETIME_PARAMS, read_only=True)
    date = serializers.DateTimeField(**SERIALIZER_DATETIME_PARAMS)
    items = ReceiptItemSerializer(many=True)
    shop_pk = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()

    class Meta:
        model = ReceiptScanning
        fields = (
            "pk",
            "user",
            "created",
            "qr_raw",
            "organization",
            "retail_place_addres",
            "organization_inn",
            "date",
            "request_number",
            "operator",
            "total_sum",
            "html",
            "shop_pk",
            "shop_name",
            "items",
        )

    @atomic
    def create(self, validated_data):
        items = validated_data.pop("items")

        instance = super().create(validated_data=validated_data)

        for item in items:
            instance.items.create(**item)

        return instance

    def get_shop_pk(self, obj: ReceiptScanning):
        # Поиск магазина из справочника по ИНН
        return Shop.objects.filter(inn=obj.organization_inn).values_list("id", flat=True).first()
    
    def get_shop_name(self, obj: ReceiptScanning):
        # Поиск магазина из справочника по ИНН
        shop_name = Shop.objects.filter(inn=obj.organization_inn).values_list("name", flat=True).first()

        return shop_name


class ReceiptScanningListSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(**SERIALIZER_DATETIME_PARAMS)
    organization = serializers.SerializerMethodField()
    date = serializers.DateTimeField(**SERIALIZER_DATETIME_PARAMS)
    is_added_check = serializers.SerializerMethodField()
    shop_pk = serializers.SerializerMethodField()

    class Meta:
        model = ReceiptScanning
        fields = (
            "pk",
            "created",
            "organization",
            "retail_place_addres",
            "organization_inn",
            "date",
            "request_number",
            "operator",
            "total_sum",
            "is_added_check",
            "shop_pk",
        )

    def get_organization(self, obj: ReceiptScanning):
        shop_name = Shop.objects.filter(inn=obj.organization_inn).values_list("name", flat=True).first()
        if shop_name:
            return shop_name
    
        return obj.organization

    def get_is_added_check(self, obj: ReceiptScanning):
        cash_check = obj.cash_check if hasattr(obj, "cash_check") else None

        if cash_check is not None:
            return True
        return False

    def get_shop_pk(self, obj: ReceiptScanning):
        # Поиск магазина из справочника по ИНН
        # TODO: Оптимизировать запрос, получить магазин в queryset
        return Shop.objects.filter(inn=obj.organization_inn).values_list("id", flat=True).first()
