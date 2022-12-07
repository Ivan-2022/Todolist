from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password", "password_repeat")

    def validate(self, initial_data):
        if initial_data['password'] != initial_data['password_repeat']:
            raise ValidationError({'password_repeat': 'Passwords must match'})
        return initial_data

    def create(self, validated_data):
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
