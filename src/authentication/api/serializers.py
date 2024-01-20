from rest_framework import serializers

from ..models import CustomUser
from ..models import UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    current_repair_object_type = serializers.SerializerMethodField()
    current_repair_object_name = serializers.SerializerMethodField()

    class Meta:
        model = UserSettings
        fields = ("current_repair_object", "current_repair_object_type", "current_repair_object_name")

    def get_current_repair_object_type(self, obj):
        if obj.current_repair_object:
            return obj.current_repair_object.type_object
        return None

    def get_current_repair_object_name(self, obj):
        if obj.current_repair_object:
            return obj.current_repair_object.name
        return None


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=5, write_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    settings = UserSettingsSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password", "is_active", "is_superuser", "first_name", "last_name", "settings")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)

        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        # instance.is_active = False
        instance.save()
        return instance

    def update(self, instance, validated_data):
        validated_data.pop("password", None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance

    def validate_username(self, value):
        if not self.instance:
            user = CustomUser.objects.filter(username=value).first()
            if user:
                raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if not self.instance:
            user = CustomUser.objects.filter(email=value).first()
            if user:
                raise serializers.ValidationError("Email already exists")
        return value
