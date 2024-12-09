from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message


# фильтр для Админа
class ChatFilter(BaseFilter):  # [1]
    def __init__(self, chat: Union[str, list]):  # [2]
        self.chat = chat

    async def __call__(self, message: Message) -> bool:  # [3]
        if isinstance(self.chat, str):
            return message.chat.id == self.chat
        else:
            return message.chat.id in self.chat
