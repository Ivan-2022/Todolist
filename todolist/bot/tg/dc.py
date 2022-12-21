from dataclasses import field
from typing import List, Optional

import marshmallow_dataclass
from marshmallow import EXCLUDE
from marshmallow_dataclass import dataclass


@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class Chat:
    id: int
    type: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    title: Optional[str] = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class Message:
    message_id: int
    from_: MessageFrom = field(metadata={"data_key": "from"})
    chat: Chat
    date: int
    text: Optional[str] = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: Message | None

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = EXCLUDE


GET_UPDATES_RESPONSE_SCHEMA = marshmallow_dataclass.class_schema(GetUpdatesResponse)()
SEND_MESSAGE_RESPONSE_SCHEMA = marshmallow_dataclass.class_schema(SendMessageResponse)()
