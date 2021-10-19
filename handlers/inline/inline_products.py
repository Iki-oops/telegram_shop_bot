from aiogram import types
from aiogram.dispatcher.filters import Regexp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db


@dp.inline_handler(text="")
@dp.inline_handler(Regexp(r'[А-Яа-яA-Za-z0-9-_]{2,100}'))
async def all_sorted_products(query: types.InlineQuery):
    results = []
    user = await db.select_user(telegram_id=int(query.from_user.id))
    if not user.get('allowed'):
        await query.answer(results=results,
                           cache_time=5,
                           switch_pm_text='Подключите бота',
                           switch_pm_parameter='connect_user')
        return

    # Из базы данных достаем все продукты и добавляем в инлайн режим
    if query.query:
        products = await db.search_product(query.query)
    else:
        products = await db.select_all_products()

    for product in products:
        product_id, title, price, photo_url, description = (
            product.get('id'),
            product.get('title'),
            product.get('price'),
            product.get('photo_url'),
            product.get('description')
        )
        markup = InlineKeyboardMarkup()
        markup.insert(
            InlineKeyboardButton(
                text='Показать товар',
                url=f'https://t.me/V_marketbot?start=product_{product_id}'
            )
        )
        results.append(
            types.InlineQueryResultArticle(
                id=str(product_id),
                title=title,
                input_message_content=types.InputTextMessageContent(
                    message_text=f'Вы выбрали {title}: {price} руб',
                    parse_mode='HTML'
                ),
                reply_markup=markup,  # Поменять инлайн кнопку
                thumb_url=photo_url,
                description=f'Цена - {price} руб.\n{description}',
            )
        )
    await query.answer(results, cache_time=5)
