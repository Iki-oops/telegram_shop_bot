from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check_button = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton('Ввести код приглашения', callback_data='invite'),
            InlineKeyboardButton('Проверить подписку',
                                 callback_data='check_subs')
        ]
    ]
)
