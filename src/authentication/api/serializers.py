import email
from rest_framework import serializers

from ..models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=5, write_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password", "is_active", "is_superuser", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)

        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        # instance.is_active = False
        instance.save()
        return instance

    def validate_username(self, value):
        user = CustomUser.objects.filter(username=value).first()
        if user:
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        user = CustomUser.objects.filter(email=value).first()
        if user:
            raise serializers.ValidationError("Email already exists")
        return value