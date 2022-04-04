from rest_framework import serializers

from app.serializers import CurrentUserDefault

from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Category
        fields = (
            "pk",
            "user",
            "name",
        )
