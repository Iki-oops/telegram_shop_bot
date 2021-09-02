from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsValidUrl(BoundFilter):
    async def check(self, message: types.Message):
        link = message.text
        if len(link) < 5:
            return False
        print(link[-4:])
        return True if link[-4:] == '.jpg' else False
