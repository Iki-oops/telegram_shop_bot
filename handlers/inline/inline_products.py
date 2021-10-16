from aiogram import types
from aiogram.dispatcher.filters import Regexp

from loader import dp, db


@dp.inline_handler(text="")
async def all_sorted_products(query: types.InlineQuery):
    results = []
    products = await db.select_all_products()
    # Из базы данных достаем все продукты и добавляем в инлайн режим
    for product in products:
        results.append(
            types.InlineQueryResultArticle(
                id=str(product.get('id')),
                title=product.get('title'),
                input_message_content=types.InputTextMessageContent(
                    message_text='Не надо было нажимать на кнопку!',
                    parse_mode='HTML'
                ),
                thumb_url=product.get('photo_url'),
                description=f'Цена - {product.get("price")} руб.\n{product.get("description")}',
            )
        )
    await query.answer(results, cache_time=5)


@dp.inline_handler(Regexp(r'[А-Яа-яA-Za-z0-9-_]{2,100}'))
async def search_product(query: types.InlineQuery):
    results = []
    products = await db.search_product(query.query)
    print(query.query)
    print(db.select_all_products(), db.select_all_users())
    print(products)
    for product in products:
        results.append(
            types.InlineQueryResultArticle(
                id=str(product.get('id')),
                title=product.get('title'),
                input_message_content=types.InputTextMessageContent(
                    message_text='Не надо было нажимать',
                    parse_mode='HTML'
                ),
                thumb_url=product.get('photo_url'),
                description=f'Цена - {product.get("price")} руб.\n{product.get("description")}',
            )
        )
    await query.answer(results, cache_time=5)
