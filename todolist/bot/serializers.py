from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TgUser
        fields = ("tg_chat_id", "tg_user_id", "username", "verification_code")

    def validate(self, attrs):
        verification_code = attrs.get("verification_code")
        tg_user = TgUser.objects.filter(verification_code=verification_code).first()
        if not tg_user:
            raise ValidationError({"verification_code": "field is incorrect"})
        attrs["tg_user"] = tg_user
        return attrs
