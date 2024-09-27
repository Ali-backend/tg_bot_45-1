import logging
from aiogram.utils import executor
from config import bot, dp, admin
from handlers import commands, echo, quiz, FSM_reg, fsm_store, webapp, admin_group, group, send_products, delete_products
from db import db_main
from buttons import start_test

async def on_startup(_):
    for i in admin:
        await bot.send_message(chat_id=i, text="Бот включен!",
                               )
        await db_main.sql_create()






commands.register_commands(dp)
quiz.register_quiz(dp)
FSM_reg.register_fsm_reg(dp)
fsm_store.register_store(dp)
webapp.register_handlers_webapp(dp)
group.register_group(dp)
send_products.register_send_products_handler(dp)
delete_products.register_send_delete_product(dp)


admin_group.register_admin_group(dp)
# echo.register_echo(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
admin_group.register_admin_group(dp)
# echo.register_echo(dp)


