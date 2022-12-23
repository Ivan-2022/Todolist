from django.conf import settings
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient


class VerificationView(GenericAPIView):
    model = TgUser
    permission_classes = [IsAuthenticated]
    serializer_class = TgUserSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tg_user = serializer.validated_data["tg_user"]
        tg_user.user = self.request.user
        tg_user.save(update_fields=["user"])
        instance_serializer: TgUserSerializer = self.get_serializer(tg_user)
        TgClient(settings.BOT_API_TOKEN).send_message(tg_user.tg_chat_id, "Подтверждение - успешно")

        return Response(instance_serializer.data, status=status.HTTP_200_OK)
