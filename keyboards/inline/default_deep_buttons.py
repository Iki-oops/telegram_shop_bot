from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

menu_cd = CallbackData('show', 'level', 'start', 'head', 'body', 'foot')


def make_callback_data(level, start='0', head='0', body='0', foot='0'):
    return menu_cd.new(level=level, start=start, head=head, body=body, foot=foot)


async def head_keyboard(start, **kwargs):
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)
    for item in kwargs:
        callback_data = make_callback_data(level=CURRENT_LEVEL+1, start=start, head=item)
        markup.insert(
            InlineKeyboardButton(
                text=kwargs[item],
                callback_data=callback_data
            )
        )
    return markup


async def body_keyboard(start, head, **kwargs):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=2)
    for item in kwargs:
        markup.insert(
            InlineKeyboardButton(
                text=kwargs[item],
                callback_data=make_callback_data(level=CURRENT_LEVEL+1, start=start, head=head, body=item)
            )
        )
    markup.row(InlineKeyboardButton(text='Назад', callback_data=make_callback_data(level=CURRENT_LEVEL-1, start=start)))
    return markup


async def foot_keyboard(start, head, body, **kwargs):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=2)
    for item in kwargs:
        markup.insert(
            InlineKeyboardButton(
                text=kwargs[item],
                callback_data=make_callback_data(level=CURRENT_LEVEL+1, start=start, head=head, body=body, foot=item)
            )
        )
    markup.row(InlineKeyboardButton(text='Назад', callback_data=make_callback_data(level=CURRENT_LEVEL-1, start=start,
                                                                                   head=head)))
