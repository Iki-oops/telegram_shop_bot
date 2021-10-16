from typing import Union

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from handlers.users.not_registred import list_for_register
from keyboards.inline.default_deep_buttons import menu_cd, body_keyboard
from keyboards.inline.to_inline_mode import menu_start
from loader import dp, db
from utils.misc.acl_decorator import allow


@allow()
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await db.select_user(message.from_user.id)
    if user.get('allowed'):
        await list_head(message)
    else:
        await list_for_register(message)


async def list_head(message: Union[types.Message, types.CallbackQuery]):
    markup = menu_start
    text = f"""
Привет👋.

Я умею <b>показывать каталог товаров и принимать оплату👩‍💼</b>

Здесь работает реферальная система:
Ты можешь пригласить кого-угодно и получить за это\n10💵 на покупку любого товара.🤑

Чтобы начать, нажми на кнопку ниже👇
    """
    if isinstance(message, types.Message):
        await message.answer(text=text, reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(menu_cd.filter(level='0', start='menu_registered', head='0', body='0', foot='0'))
async def get_start(call: types.CallbackQuery):
    await list_head(call)


@dp.callback_query_handler(menu_cd.filter(level='1', start='menu_registered', head='profile', body='0', foot='0'))
async def get_profile(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    data = await db.select_user(int(call.from_user.id))
    markup = await body_keyboard(start=callback_data.get('start'), head=callback_data.get('head'))
    await call.message.edit_text(f'Рады видеть вас, {data.get("name")}\n\n'
                                 f'🔅Telegram ID: {data.get("telegram_id")}\n'
                                 f'💴Остаток: {70 * data.get("money")} рублей',
                                 reply_markup=markup)
