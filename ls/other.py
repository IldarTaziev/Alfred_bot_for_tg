from aiogram import types, Dispatcher


# ------ Остальное ------
# @dp.message_handler(commands=["ситуация_на_дароге"])
async def weather(message: types.Message):
    await message.answer("Простите в этом я бессилен!")


# @dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(weather, commands=['ситуация_на_дароге'])
    dp.register_message_handler(echo)
