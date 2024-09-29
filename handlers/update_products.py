import sqlite3
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class EditProductsState(StatesGroup):
    waiting_for_field = State()
    waiting_for_new_value = State()
    waiting_for_photo = State()


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


def update_products_field(product_id, field_name, new_value):
    products_table = ['name_products', 'size', 'price', 'photo']
    products_details_table = ['category', 'info_product']

    conn = get_db_connection()

    try:
        if field_name in products_table:
            query = f"UPDATE products SET {field_name} = ? WHERE product_id = ?"
        elif field_name in products_details_table:
            query = f"UPDATE products_detail SET {field_name} = ? WHERE product_id = ?"
        else:
            raise ValueError(f'Недопустимое имя поля: {field_name}')

        conn.execute(query, (new_value, product_id))
        conn.commit()

    except sqlite3.OperationalError as e:
        print(f"Ошибка: {e}")

    finally:
        conn.close()


async def start_sending_products(message: types.Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    button = InlineKeyboardButton('Посмотреть', callback_data='show_all_update')
    keyboard.add(button)

    await message.answer('Нажмите на кнопку для отправки всех товаров!', reply_markup=keyboard)


async def send_all_products(callback_query: types.CallbackQuery):
    products = fetch_all_products()

    if products:
        for product in products:
            keyboard = InlineKeyboardMarkup(resize_keyboard=True)
            button = InlineKeyboardButton('Редактировать', callback_data=f"edit_{product['product_id']}")
            keyboard.add(button)

            caption = (f'Артикул - {product["product_id"]}\n'
                       f'Название - {product["name_products"]}\n'
                       f'Информация - {product["info_product"]}\n'
                       f'Категория - {product["category"]}\n'
                       f'Размер - {product["size"]}\n'
                       f'Цена - {product["price"]} сом')

            await callback_query.message.answer_photo(photo=product['photo'],
                                                      caption=caption,
                                                      reply_markup=keyboard)
    else:
        await callback_query.message.answer('Товары не найдены')


async def edit_product_callback(callback_query: types.CallbackQuery, state: FSMContext):
    product_id = callback_query.data.split('_')[1]

    await state.update_data(product_id=product_id)

    keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)

    name_button = InlineKeyboardButton(text="Название", callback_data="field_name_product")
    category_button = InlineKeyboardButton(text="Категория", callback_data="field_category")
    price_button = InlineKeyboardButton(text="Цена", callback_data="field_price")
    size_button = InlineKeyboardButton(text="Размер", callback_data="field_size")
    photo_button = InlineKeyboardButton(text="Фото", callback_data="field_photo")
    info_button = InlineKeyboardButton(text="Инфо о товаре", callback_data="field_info_product")

    keyboard.add(name_button, category_button, price_button, size_button, photo_button, info_button)

    await callback_query.message.answer('Выберите поле для редактирования:', reply_markup=keyboard)
    await EditProductsState.waiting_for_field.set()


async def select_field_callback(callback_query: types.CallbackQuery, state: FSMContext):
    field_map = {
        "field_name_product": "name_products",
        "field_category": "category",
        "field_price": "price",
        "field_size": "size",
        "field_photo": "photo",
        "field_info_product": "info_product"
    }

    field = field_map.get(callback_query.data)

    if not field:
        await callback_query.message.answer('Недопустимое поле')
        return

    await state.update_data(field=field)

    if field == 'photo':
        await callback_query.message.answer('Отправьте новое фото:')
        await EditProductsState.waiting_for_photo.set()

    else:
        await callback_query.message.answer(f'Введите новое значения для поля {field}:')
        await EditProductsState.waiting_for_new_value.set()


async def set_new_value(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    product_id = user_data['product_id']
    field = user_data['field']
    new_value = message.text

    update_products_field(product_id, field, new_value)

    await message.answer(f'Поле {field} успешно обновлено!')
    await state.finish()


async def set_new_photo(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    product_id = user_data['product_id']

    photo_id = message.photo[-1].file_id

    update_products_field(product_id, 'photo', photo_id)

    await message.answer('Фото успешно обновлено!')
    await state.finish()


def register_update_products_handlers(dp: Dispatcher):
    dp.register_message_handler(start_sending_products, commands=['products_update'])
    dp.register_callback_query_handler(send_all_products, Text(equals='show_all_update'))
    dp.register_callback_query_handler(edit_product_callback, Text(startswith='edit_'), state='*')
    dp.register_callback_query_handler(select_field_callback, Text(startswith='field_'),
                                       state=EditProductsState.waiting_for_field)
    dp.register_message_handler(set_new_value, state=EditProductsState.waiting_for_new_value)
    dp.register_message_handler(set_new_photo, content_types=['photo'], state=EditProductsState.waiting_for_photo)




