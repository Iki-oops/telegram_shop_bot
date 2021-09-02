from aiogram import types
from aiogram.dispatcher.filters import Regexp

from loader import dp, db


@dp.inline_handler(text="")
async def all_sorted_products(query: types.InlineQuery):
    results = []
    products = db.select_all_products()
    # Из базы данных достаем все продукты и добавляем в инлайн режим
    for product in products:
        results.append(
            types.InlineQueryResultArticle(
                id=str(product[0]),
                title=product[1],
                input_message_content=types.InputTextMessageContent(
                    message_text='Не надо было нажимать на кнопку!',
                    parse_mode='HTML'
                ),
                thumb_url=product[4],
                description=f'Цена - {product[3]} руб.\n{product[2]}',
            )
        )
    await query.answer(results, cache_time=5)


@dp.inline_handler(Regexp(r'[А-Яа-яA-Za-z0-9-_]{2,100}'))
async def search_product(query: types.InlineQuery):
    results = []
    products = db.search_product(query.query)
    print(query.query)
    print(db.select_all_products(), db.select_all_users())
    print(products)
    for product in products:
        results.append(
            types.InlineQueryResultArticle(
                id=str(product[0]),
                title=product[1],
                input_message_content=types.InputTextMessageContent(
                    message_text='Не надо было нажимать',
                    parse_mode='HTML'
                ),
                thumb_url=product[4],
                description=f'Цена - {product[3]} руб.\n{product[2]}',
            )
        )
    await query.answer(results, cache_time=5)
