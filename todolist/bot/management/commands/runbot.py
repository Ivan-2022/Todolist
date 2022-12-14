import os
from enum import Enum, unique, auto
from typing import Optional

from django.core.management import BaseCommand
from marshmallow_dataclass import dataclass

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, Category
from todolist import settings


@dataclass
class NewGoal:
    cat_id: Optional[int] = None
    goal_title: Optional[str] = None

    def complete(self) -> bool:
        return None not in {self.cat_id, self.goal_title}


@unique
class StateEnum(Enum):
    CATEGORY_STATE = auto()
    CHOSEN_CATEGORY = auto()
    VIEW_GOALS_LIST = auto()


@dataclass
class FSMData:
    state: StateEnum
    goal: NewGoal


FSM_STATES: dict[int, FSMData] = dict()


class Command(BaseCommand):
    help = 'Функционал телеграм-бота'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_API_TOKEN)
        self.offset = 0

    @staticmethod
    def _generate_verification_code() -> str:
        """ Генерирует случайный пароль """
        return os.urandom(12).hex()

    def handle_user_without_verification(self, msg: Message, tg_user: TgUser):
        """ Верификация пользователя """
        code = self._generate_verification_code()
        tg_user.verification_code = code
        tg_user.save(update_fields=['verification_code'])

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f" Для подтверждения своего аккаунта необходимо ввести код {code} на сайте"
        )

    def handle_goals_list(self, msg: Message, tg_user: TgUser):
        """ Получение списка целей пользователя """
        goals_list = '\n'.join([f'{goal.title}' for goal in Goal.objects.filter(
            category__board__participants__user_id=tg_user.user_id,).exclude(status=Goal.Status.archived)])
        self.tg_client.send_message(msg.chat.id, f'список ваших целей:\n {goals_list}' or "Список целей пуст")

    def handle_categories_list(self, msg: Message, tg_user: TgUser):
        """ Получение списка категорий для создания новой цели"""
        category_list = [f'{cat.title}' for cat in Category.objects.filter(
            board__participants__user_id=tg_user.user_id,
            is_deleted=False)]
        if category_list:
            self.tg_client.send_message(msg.chat.id, "выберите категорию\n{}".format("\n".join(category_list)))
        else:
            self.tg_client.send_message(msg.chat.id, "категории не найдены")

    def handle_save_category(self, msg: Message, tg_user: TgUser):
        """ Выбор категории для создания новой цели"""
        if msg.text:
            title = msg.text
            new_goal = Category.objects.filter(board__participants__user_id=tg_user.user_id,
                                               is_deleted=False,
                                               title=title).first()
            if new_goal:
                FSM_STATES[tg_user.chat_id].goal.cat_id = new_goal.id
                self.tg_client.send_message(msg.chat.id, "введите название цели для ее создания")
                FSM_STATES[tg_user.chat_id].state = StateEnum.CHOSEN_CATEGORY
                return
        self.tg_client.send_message(msg.chat.id, "такой категории нет")

    def handle_save_new_goal(self, msg: Message, tg_user: TgUser):
        """ Создание новой цели """
        goal: NewGoal = FSM_STATES[tg_user.chat_id].goal
        goal.goal_title = msg.text
        if goal.complete():
            Goal.objects.create(
                title=goal.goal_title,
                category_id=goal.cat_id,
                user_id=tg_user.user_id
            )
            self.tg_client.send_message(msg.chat.id, f"новая цель {goal.goal_title} создана")
        else:
            self.tg_client.send_message(msg.chat.id, "что-то пошло не так")

        FSM_STATES.pop(tg_user.chat_id, None)

    def handle_verified_user(self, msg: Message, tg_user: TgUser):
        """ Работа с доступными верифицированному пользователю командами """
        if not msg.text:
            return
        if "goals" in msg.text:
            self.handle_goals_list(msg=msg, tg_user=tg_user)
            FSM_STATES[tg_user.chat_id] = FSMData(state=StateEnum.VIEW_GOALS_LIST, goal=None)

        elif "create" in msg.text:
            self.handle_categories_list(msg=msg, tg_user=tg_user)
            FSM_STATES[tg_user.chat_id] = FSMData(state=StateEnum.CATEGORY_STATE, goal=NewGoal())

        elif "cancel" in msg.text and tg_user.chat_id in FSM_STATES:
            FSM_STATES.pop(tg_user.chat_id)
            self.tg_client.send_message(msg.chat.id, "операция прервана, введите команду")

        elif tg_user.chat_id in FSM_STATES:
            state: StateEnum = FSM_STATES[tg_user.chat_id].state

            if state == StateEnum.CATEGORY_STATE:
                self.handle_save_category(msg=msg, tg_user=tg_user)

            elif state == StateEnum.CHOSEN_CATEGORY:
                self.handle_save_new_goal(msg=msg, tg_user=tg_user)

        else:
            self.tg_client.send_message(msg.chat.id, "неизвестная команда")

        print(FSM_STATES)

    def handle_message(self, msg: Message):
        """ Проверка наличия пользователя и выдача верификационного ключа новому пользователю """
        tg_user, created = TgUser.objects.get_or_create(
            chat_id=msg.chat.id,
            defaults={
                "username": msg.from_.username,
            },
        )
        if created:
            self.tg_client.send_message(msg.chat.id, "Здравствуйте")

        if tg_user.user:
            self.handle_verified_user(msg, tg_user)

        else:
            self.handle_user_without_verification(msg, tg_user)

    def handle(self, *args, **options):
        """ Запуск бота """
        while True:
            res = self.tg_client.get_updates(offset=self.offset)
            for item in res.result:
                self.offset = item.update_id + 1
                self.handle_message(item.message)
