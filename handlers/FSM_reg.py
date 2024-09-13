from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
import logging




logging.basicConfig(level=logging.INFO)



class FSMRegistration(StatesGroup):
    date = State()


dp.message_handler(commands='register')
async def cmd_register(message: types.Message):
    await message.answer('Введите дату рождения: ')
    await FSMRegistration.date.set()


dp.message_handler(state=FSMRegistration.date)
async def process_date(message: types.Message, state: FSMContext):
    date_of_birth = message.text

    await message.answer(f'Дата рождения сохранена: {date_of_birth}')
    await state.finish()


