from django.core.management import BaseCommand

from bot.tg.client import TgClient
from todolist import settings


class Command(BaseCommand):
    tg_client = TgClient(settings.BOT_API_TOKEN)

    def handle(self, *args, **options):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                print(item.message)
