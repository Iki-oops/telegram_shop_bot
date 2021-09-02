from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import CHANNELS
from keyboards.inline.default_deep_buttons import head_keyboard, menu_cd, body_keyboard
from keyboards.inline.to_inline_mode import to_inline_mode
from loader import dp, db, bot
from states.invite_state import Invite
from utils.misc.acl_decorator import allow
from utils.misc.checker_sub import check


async def list_for_register(message: Union[types.Message, types.CallbackQuery]):
    markup = await head_keyboard(start='not_registered', invite='Ввести код приглашения',
                                 check_sub='Проверить подписку')
    result = str()
    for num, channel in enumerate(CHANNELS, start=1):
        chat = await dp.bot.get_chat(channel)
        link = await chat.export_invite_link()
        result += f"{num}) <a href='{link}'>{chat.title}</a>\n"
    text = f"""
У вас нет доступа к боту🚫

Чтобы использовать этого бота введите код приглашения📩,
либо пройдите по реферальной ссылке
Также можно получить бота подписавшись на наши каналы:
{result}
Выберите нужный вам метод активации бота👇
"""
    if isinstance(message, types.Message):
        await message.answer(text, reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(menu_cd.filter(level='0', start='not_registered', head='0', body='0', foot='0'))
async def get_no_registered_start(call: types.CallbackQuery):
    await call.answer()
    await list_for_register(call)


@dp.callback_query_handler(menu_cd.filter(level='0', start='not_registered', head='0', body='0', foot='0'),
                           state=Invite.I1)
async def tap_button_with_state(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    await list_for_register(call)


@dp.callback_query_handler(menu_cd.filter(level='1', start='not_registered', head='invite', body='0', foot='0'))
async def write_invite(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    markup = await body_keyboard(start=callback_data.get('start'), head=callback_data.get('head'))
    await call.message.edit_text('Напишите мне код приглашения',
                                 reply_markup=markup)
    await Invite.first()


@allow(state=True)
@dp.message_handler(state=Invite.I1)
async def invite_code(message: types.Message, state: FSMContext):
    referrer = db.select_user(message.text)
    if referrer:
        money = referrer[4] + 10
        db.update_user(referrer[0], money=money)
        db.update_user(message.from_user.id, allowed=1)
        await message.answer('Код приглашения сработал.\nВам доступен бот👩‍💼\n'
                             'Нажми на кнопку, чтобы начать смотреть на каталог товаров👇',
                             reply_markup=to_inline_mode)
    else:
        await message.answer('К сожалению, код недействителен🚫')
    await state.finish()


@dp.callback_query_handler(menu_cd.filter(level='1', start='not_registered', head='check_sub', body='0', foot='0'))
async def check_subs(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    result_sub = list()
    result_no_sub = list()
    markup = await body_keyboard(start=callback_data.get('start'), head=callback_data.get('head'))
    all_subs = True
    for value, channel in enumerate(CHANNELS, start=1):
        status = await check(call.from_user.id, channel)
        channel = await bot.get_chat(channel)
        link = await channel.export_invite_link()
        if status:
            result_sub.append(f'{value}) <a href="{link}">{channel.title}</a>')
        else:
            all_subs = False
            result_no_sub.append(f'{value}) <a href="{link}">{channel.title}</a>')

    if all_subs:
        return await call.message.edit_text('Подписка на все каналы оформлена☺️.\n'
                                            'Вам доступен бот.\n'
                                            'Нажми на кнопку, чтобы начать смотреть на каталог товаров👇',
                                            reply_markup=to_inline_mode)
    elif len(result_sub) == 0:
        return await call.message.edit_text(
            '\n'.join(
                ['Вы не подписались ни на один из каналов:\n'] + result_no_sub
            ),
            disable_web_page_preview=True,
            reply_markup=markup
        )
    await call.message.answer(
        '\n'.join(
            ['Каналы, на которые вы подписались:\n'] + result_sub + ['Каналы на которые не подписались:\n'] + result_no_sub
        ),
        disable_web_page_preview=True,
        reply_markup=markup
    )
