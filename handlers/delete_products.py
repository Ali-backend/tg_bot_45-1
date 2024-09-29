import sqlite3
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.dispatcher.filters import Text


def get_db_connection():
    conn = sqlite3.connect('db/store.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
    SELECT * FROM products p 
    INNER JOIN products_detail pd ON p.product_id = pd.product_id 
    """).fetchall()
    conn.close()
    return products


def delete_product(product_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
    conn.commit()
    conn.close()


async def start_sending_products(message: types.Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    show_all_products_delete = InlineKeyboardButton(text='Посмотреть',
                                                    callback_data='show_all_delete')
    keyboard.add(show_all_products_delete)

    await message.answer('Для просмотра товаров, нажмите на кнопку ниже!',
                         reply_markup=keyboard)


async def send_all_products(callback_query: types.CallbackQuery):
    products = fetch_all_products()

    if products:
        for product in products:
            caption = (f'Название товара - {product["name_products"]}\n'
                       f'Информация о товаре - {product["info_product"]}\n'
                       f'Категория - {product["category"]}\n'
                       f'Размер - {product["size"]}\n'
                       f'Цена - {product["price"]}\n'
                       f'Артикул - {product["product_id"]}\n')

            delete_product_markup = InlineKeyboardMarkup(resize_keyboard=True)
            delete_product_button = InlineKeyboardButton('Удалить',
                                                         callback_data=f'delete_{product["product_id"]}')
            delete_product_markup.add(delete_product_button)

            await callback_query.message.answer_photo(photo=product['photo'],
                                                      caption=caption,
                                                      reply_markup=delete_product_markup)
    else:
        await callback_query.message.answer(text='В базе товаров нет!')


async def delete_products_callback(callback_query: types):
    product_id = int(callback_query.data.split("_")[1])

    delete_product(product_id)
    await callback_query.answer("Товар удален")

    if callback_query.message.photo:
        new_caption = "Товар был удалён. Обновите список товаров!"

        photo_404 = open('media/img_404.png', 'rb')

        await callback_query.message.edit_media(
            InputMediaPhoto(media=photo_404,
                            caption=new_caption))
    else:
        await callback_query.message.edit_text('Товар был удалён. Обновите список товаров!')


def register_delete_product_handler(dp: Dispatcher):
    dp.register_message_handler(start_sending_products, commands=['products_del'])
    dp.register_callback_query_handler(send_all_products, Text(equals='show_all_delete'))
    dp.register_callback_query_handler(delete_products_callback, Text(startswith='delete_'))

