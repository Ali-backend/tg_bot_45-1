# from aiogram import types, Dispatcher
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import Text
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.utils import executor
#
#
# class StoreFSM(StatesGroup):
#     waiting_for_item_name = State()
#     waiting_for_size = State()
#     waiting_for_category = State()
#     waiting_for_price = State()
#     waiting_for_photo = State()
#
#
# async def cmd_start(message: types.Message):
#     await message.answer('Введите название товара')
#     await StoreFSM.waiting_for_item_name.set()
#
#
# async def start_reg(message: types.Message):
#     await message.answer('Здраствуйте! /n'
#                          'Введите название кофты: ')
#     await fsm_registration.fullname.set()
#
# async def load_name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['fullname'] = message.text
#
#     await message.answer('Введите дату рождения: ')
#     await fsm_registration.date.set()
#
# async def load_date(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['date'] = message.text
#
#         await message.answer('Верны ли данные?')
#         await message.answer(f'ФИО: {data["fullname"]}')