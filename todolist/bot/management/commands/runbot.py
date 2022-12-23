import os

from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from todolist import settings


class Command(BaseCommand):
    tg_client = TgClient(settings.BOT_API_TOKEN)

    @staticmethod
    def _generate_verification_code() -> str:
        return os.urandom(12).hex()

    def handle_user_without_verification(self, msg: Message, tg_user: TgUser):
        code: str = self._generate_verification_code()
        tg_user.verification_code = code
        tg_user.save(update_fields=['verification_code'])

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f" Для подтверждения своего аккаунта необходимо ввести код {code} на сайте")

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            tg_chat_id=msg.chat.id,
            defaults={"username": msg.from_.username})
        if created:
            self.tg_client.send_message(msg.chat.id, "Здравствуйте")
        else:
            self.handle_user_without_verification(msg, tg_user)

    def handle(self, *args, **options):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)
