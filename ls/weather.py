from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove

import API
import keyboard


# @dp.message_handler(commands=["погода"])
async def weather(message: types.Message):
    a = ReplyKeyboardRemove()
    situation = API.weather()
    await message.answer(
        f"Мне сказали что на улице {situation['Status']}\nВышел сам. чувствуется как {situation['Temperature']}\nСкорость ветра кстати {situation['Wind_Speed']} m/s",
        reply_markup=a)
    await message.answer("Можете проверить сами!", reply_markup=keyboard.weather)


def register_handlers_weather(dp: Dispatcher):
    dp.register_message_handler(weather, commands=["weather"])
