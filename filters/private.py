from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import ADMINS


class IsPrivateAdmin(BoundFilter):
    async def check(self, message: types.Message):
        if str(message.from_user.id) in ADMINS:
            return message.chat.type == types.ChatType.PRIVATE
