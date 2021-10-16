from aiogram import types
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from asyncpg.exceptions import UniqueViolationError

from data.config import ADMINS, CHANNELS
from loader import db
from utils.misc.checker_sub import check


class BigBrother(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_id = int(message.from_user.id)
        name = message.from_user.first_name
        try:
            referrer_id = int(message.get_args())
        except (AttributeError, ValueError, TypeError):
            referrer_id = None
        try:
            # Ничего не возвращает(None)
            user = await db.add_user(user_id, name, False)
        except UniqueViolationError:
            user = await db.select_user(user_id)

        if user_id in ADMINS and not user and False:
            await db.update_user(user_id, allowed=True)
        elif referrer_id:
            referrer = await db.select_user(referrer_id)
            if referrer:
                money = referrer.get('money') + 10
                await db.update_user(referrer_id, money=money)
                await db.update_user(user_id, allowed=True, money=10)
        else:
            subscription = True
            for channel in CHANNELS:
                if await check(user_id, channel):
                    continue
                subscription = False
            if subscription:
                await db.update_user(user_id, allowed=True)
        data['user'] = await db.select_user(message.from_user.id)

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        if not handler:
            return
        allow = getattr(handler, 'allow', False)
        state = getattr(handler, 'state', False)
        allowed = data.get('user').get('allowed')
        if (allow and not allowed) or allowed or state:
            return
        raise CancelHandler()

        # sub_bool = True
        # user_id = message.from_user.id
        # for channel in CHANNELS:
        #     if await check(user_id, channel):
        #         continue
        #     sub_bool = False
        # try:
        #     referrer = await db.select_user(message.get_args())
        #     if not referrer:
        #         referrer_id = None
        #     else:
        #         referrer_id = referrer[0]
        #         money = referrer[4] + 10
        #         await db.update_user(referrer_id, money=money)
        #
        #     if referrer_id or user_id in ADMINS or sub_bool:
        #         await db.add_user(user_id, message.from_user.full_name, allowed=1,
        #                           referrer=referrer_id, money=10)
        #     else:
        #         await db.add_user(user_id, message.from_user.full_name)
        # except UniqueViolationError:
        #     user = await db.select_user(message.from_user.id)
        #     print(user)
        #     if (sub_bool or message.from_user.id in ADMINS) and not user[2]:
        #         await db.update_user(user_id, allowed=1)