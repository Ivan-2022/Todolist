from rest_framework import serializers
from .models import Category
from ..core.serializers import ProfileSerializer


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")