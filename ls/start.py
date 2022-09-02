from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import keyboard
from db_f import ex_users, db_add_user, db_add_new_schedule, db_add_weekdays
from conf import weekdays


# ------ Сценарии ------
class StartSchedule(StatesGroup):
    id_name_lastname_username = State()
    group = State()


# ------ Самое начало общения с новым пользователем ! ------
# @dp.message_handler(commands=["start"], state=None)
async def start(message: types.Message):
    users = ex_users()
    is_in_list = False
    for row in users:
        if row[0] == message.from_user.id:
            is_in_list = True
    if is_in_list is True:
        await message.answer("Вы уже прошли начальный этап")
        await message.answer("Лучше напишите /help или /menu!")
    else:
        await StartSchedule.id_name_lastname_username.set()
        text = f"Приветствю вас у себя {message.from_user.first_name}!\nМоё имя Альфред.\nСкажите как я могу вас называть?"
        await message.answer(text)


# @dp.message_handler(state=StartSchedule.id_name_lastname_username)
async def set_id(message: types.Message, state: FSMContext):
    await state.update_data(id=message.from_user.id)
    await state.update_data(name=message.from_user.first_name)
    await state.update_data(lastname=message.from_user.last_name)
    await state.update_data(username=message.text)
    await message.answer(f"Понял буду звать вас{message.text}\nТеперь скажите вашу группу.")
    await message.answer(f"Пример: 1IS02")
    await StartSchedule.group.set()


# @dp.message_handler(state=StartSchedule.group)
async def set_group(message: types.Message, state: FSMContext):
    group_text = message.text.upper()
    await state.update_data(group=group_text)
    data = await state.get_data()
    tg_id = data['id']
    name = data['name']
    last_name = data['lastname']
    username = data['username']
    group = data['group']
    db_add_user(tg_id, name, last_name, username, group)
    db_add_new_schedule(group)
    db_add_weekdays(weekdays)
    await message.answer("Все!\nЯ вас запомнил.\nТеперь можете посмотреть на список команд", reply_markup=keyboard.menu)
    await message.answer("Если забудете команды, то всегда можете написать /help или /menu!")
    await state.finish()


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(set_id, state=StartSchedule.id_name_lastname_username)
    dp.register_message_handler(set_group, state=StartSchedule.group)