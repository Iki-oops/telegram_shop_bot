from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.default_deep_buttons import make_callback_data

to_inline_mode = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('🧩Выбрать товар', switch_inline_query_current_chat='')
        ]
    ]
)

menu_start = to_inline_mode
callback_data = make_callback_data(level=1, start='menu_registered', head='profile')
menu_start.row(
    InlineKeyboardButton(
        text='🧑‍💻Профиль', callback_data=callback_data
    )
)
