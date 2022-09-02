from aiogram import types, Dispatcher

import keyboard
from conf import bot


# ------ функции для команд или определённого текста ------
# @dp.message_handler(commands=["help", "menu"])
async def help_comm(message: types.Message):
    await bot.send_message(message.from_user.id, "Чем вам помочь?", reply_markup=keyboard.menu)


# @dp.message_handler(commands=["status"])
async def status(message: types.Message):
    await bot.send_message(message.from_user.id, "Я всё ещё разрабатываюсь.")


def register_handlers_default(dp: Dispatcher):
    dp.register_message_handler(help_comm, commands=["help", "menu"])
    dp.register_message_handler(status, commands=["status"])
