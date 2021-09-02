import logging
import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import counter_products
from filters import IsPrivateAdmin, IsValidUrl
from keyboards.inline.to_inline_mode import to_inline_mode
from loader import dp, db
from states.create_product import Product
from utils.photo_link import photo_link


@dp.message_handler(Command('add_product'), IsPrivateAdmin())
async def new_product(message: types.Message):
    await message.answer('Для добавления продукта, отправьте мне название продукта.')
    await Product.first()


@dp.message_handler(state=Product.P1)
async def product_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await message.answer('Отлично👍. Теперь отправь мне описание.')
    await Product.next()


@dp.message_handler(state=Product.P2)
async def product_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await message.answer('Хорошо, теперь цену товара в рублях.')
    await Product.next()


@dp.message_handler(state=Product.P3)
async def product_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Последнее. Отправь мне фото или ссылку.🗾')
    await Product.next()


@dp.message_handler(state=Product.P4, content_types=types.ContentType.PHOTO)
@dp.message_handler(IsValidUrl(), state=Product.P4, content_types=types.ContentType.TEXT)
async def product_photo(message: types.Message, state: FSMContext):
    if message.content_type == types.ContentType.TEXT:
        link = message.text
    else:
        photo = message.photo[-1]
        link = await photo_link(photo)

    data = await state.get_data()
    title, description, price, photo_url = data.get('title'), data.get('description'), data.get('price'), link
    try:
        db.add_product(next(counter_products), title, description, price, link)
        await message.answer('Замечательно. Новый продукт создан и добавлен в базу🥇.',
                             reply_markup=to_inline_mode)
        await state.finish()
    except sqlite3.IntegrityError:
        logging.error('Ошибка уникальности. add_product')
        await message.answer('Ошибка уникальности.')


# Валидаторы
@dp.message_handler(Command('add_product'))
async def no_allow_adding(message: types.Message):
    await message.answer('У вас нет доступа к этой команде🚫')


@dp.message_handler(state=Product.P4, content_types=types.ContentType.ANY)
async def product_photo_valid(message: types.Message):
    await message.answer('Отправьте фотку, либо ссылку с расширением .jpg')


@dp.message_handler(state=[Product.P1, Product.P2, Product.P3])
async def text_valid(message: types.Message):
    await message.answer('Текстом, надо написать.')
