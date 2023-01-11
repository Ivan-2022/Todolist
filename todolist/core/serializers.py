from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
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

    def create(self, validated_data: dict) -> User:
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password")

    def create(self, validated_data: dict) -> User:
        username = validated_data['username']
        password = validated_data['password']
        user = authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, attrs: dict):
        if not self.instance.check_password(attrs['old_password']):
            raise ValidationError({'old_password': 'field is incorrect'})
        return attrs

    def update(self, instance: User, validated_data: dict) -> User:
        instance.password = make_password(validated_data['new_password'])
        instance.save(update_fields=['password'])
        return instance
