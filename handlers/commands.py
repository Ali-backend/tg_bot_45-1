import os
from aiogram.types import InputFile
from buttons import start
from config import dp, bot
from aiogram import types, Dispatcher




async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Hello!',
                           reply_markup=start)


async def info_handler(message: types.Message):
    await message.answer(text='Привет, Я бот для группы 45-1')


async def mem_handler(message: types.Message):
    folder = 'media'
    photo_path = os.path.join(folder, 'img.png')
    with open(photo_path, "rb") as photo:
        # await bot.send_photo(chat_id=message.from_user.id, photo=photo)
        await message.answer_photo(photo=photo)


async def mem_all_handler(message: types.Message):
    folder = 'media'
    photos = os.listdir(folder)

    for photo_name in photos:
        photo_path = os.path.join(folder, photo_name)

        if photo_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            with open(photo_path, 'rb') as photo:
                await message.answer_photo(InputFile(photo))


async def music_handler(message: types.Message):
    folder = 'musics'

    music_name = 'trac_1'

    music_path = os.path.join(folder, music_name)

    with open(music_path, 'rb') as music:
        await message.answer_audio(InputFile(music))









def register_commands(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(info_handler, commands=['info'])
    dp.register_message_handler(mem_handler, commands=['mem'])
    dp.register_message_handler(mem_all_handler, commands=['mem_all'])
    dp.register_message_handler(music_handler, commands=['music'])


