import re

from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import LabeledPrice

from data import config
from loader import dp, db, bot


@dp.message_handler(CommandStart(deep_link=re.compile(r'product_[0-9]+')))
async def buy_food(message: types.Message):
    product_id = message.get_args().replace('product_', '')
    product = await db.select_product(id=int(product_id))
    price = int(product.get('price')) * 100
    INVOICE_DATA = dict(
        chat_id=message.chat.id,
        title=product.get('title'),
        description=product.get('description'),
        provider_token=config.PROVIDER_TOKEN,
        currency='RUB',
        prices=[
            LabeledPrice(label='Тульский пряник', amount=price),
        ],
        payload=product.get('id') + 1000,
        start_parameter=f'create_invoice_{product.get("id")}',
        photo_url=product.get('photo_url'),
        photo_size=600,
        is_flexible=True
    )
    await bot.send_invoice(**INVOICE_DATA)


@dp.shipping_query_handler()
async def choose_shipping(query: types.ShippingQuery):
    POST_REGULAR_SHIPPING = types.ShippingOption(
            id='post_reg',
            title='Почтой',
            prices=[
                LabeledPrice(label='Обычная коробка', amount=100_00),
                LabeledPrice(label='Обычной почтой', amount=300_00),
            ]
        )
    POST_FAST_SHIPPING = types.ShippingOption(
        id='post_fast',
        title='Быстрая доставка',
        prices=[
            LabeledPrice(label='Прочная коробка', amount=200_00),
            LabeledPrice(label='Быстрая доствка за 3 дня', amount=1000_00),
        ]
    )
    if query.shipping_address.country_code == 'RU':
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[POST_REGULAR_SHIPPING,
                                                          POST_FAST_SHIPPING],
                                        ok=True)
        return
    await bot.answer_shipping_query(
        shipping_query_id=query.id,
        ok=False,
        error_message='Сюда не доставляем'
    )


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id,
                                        ok=True)
