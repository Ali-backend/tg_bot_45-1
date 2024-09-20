import logging

from aiogram import Dispatcher
from aiogram.utils import executor
from handlers import commands, echo, quiz, FSM_reg, fsm_store
from config import dp, bot, Admins
from db import db_main


async def on_startup(_):
    for admin in Admins:
        await bot.send_message(chat_id=admin, text="Бот включен!")
        await db_main.sql_create()


async def on_shutdown(_):
    for admin in Admins:
        await bot.send_message(chat_id=admin, text="Бот отключен!")


commands.register_commands(dp)
quiz.register_quiz(dp)
FSM_reg.register_fsm_reg(dp)
fsm_store.register_store(dp)


echo.register_echo(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True,
                           on_startup=on_startup, on_shutdown=on_shutdown)