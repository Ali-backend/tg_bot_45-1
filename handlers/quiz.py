from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot


async def quiz(message: types.Message):
    button_quiz = InlineKeyboardMarkup()
    button_quiz_1 = InlineKeyboardButton("Дальше...",
                                         callback_data="button_1")

    button_quiz.add(button_quiz_1)


    question = 'BMW or Mercedes ?'
    answer = ['BMW', 'Mercedes', 'Lada']

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=True,
        type='quiz',
        correct_option_id=2,
        explanation='Русский автопром',
        open_period=60,
        reply_markup=button_quiz
    )


async def quiz_2(call: types.CallbackQuery):
    button_quiz = InlineKeyboardMarkup()
    button_quiz_2 = InlineKeyboardButton('Дальше...',
                                         callback_data="button_2")
    button_quiz.add(button_quiz_2)

    question = 'Nike or Adidas'
    answer = ['Nike', 'Adidas']

    photo_quiz = open('media/img_3.png', 'rb')

    await bot.send_photo(chat_id=call.from_user.id,
                         photo=photo_quiz)

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        reply_markup=button_quiz
    )


def register_quiz(dp: Dispatcher):
    dp.register_message_handler(quiz, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, text='button_1')