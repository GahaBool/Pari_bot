from aiogram.filters import Filter
from aiogram import types
import os


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types
    

ADMIN_IDS = [int(id_) for id_ in os.getenv("ADMIN_IDS", "").split(",") if id_]

class IsAdmin(Filter):
    def __init__(self):
        pass

    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in ADMIN_IDS