import typing
from loader import bot


async def check(user_id, channel: typing.Union[int, str]):
    member = await bot.get_chat_member(channel, user_id)
    return member.is_chat_member()
