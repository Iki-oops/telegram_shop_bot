import sqlite3

from aiogram import types
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import ADMINS, CHANNELS
from loader import db
from utils.misc.checker_sub import check


class BigBrother(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        sub_bool = True
        user_id = message.from_user.id
        for channel in CHANNELS:
            if await check(user_id, channel):
                continue
            sub_bool = False
        try:
            referrer = db.select_user(message.get_args())
            if not referrer:
                referrer_id = None
            else:
                referrer_id = referrer[0]
                money = referrer[4] + 10
                db.update_user(referrer_id, money=money)

            if referrer_id or user_id in ADMINS or sub_bool:
                db.add_user(user_id, message.from_user.full_name, allowed=1,
                            referrer=referrer_id, money=10)
            else:
                db.add_user(user_id, message.from_user.full_name)
        except sqlite3.IntegrityError:
            user = db.select_user(message.from_user.id)
            if (sub_bool or message.from_user.id in ADMINS) and not user[2]:
                db.update_user(user_id, allowed=1)
        data['user'] = db.select_user(message.from_user.id)

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        if not handler:
            return
        allow = getattr(handler, 'allow', False)
        state = getattr(handler, 'state', False)
        user = data.get('user')
        if user[2] or (allow and not user[2]) or state:
            return
        else:
            raise CancelHandler()
