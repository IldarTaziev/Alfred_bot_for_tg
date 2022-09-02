from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from conf import weekdays
from db_f import ex_group, db_check, db_add_lesson, db_del_lesson
import keyboard


# ------ Сценарии ------
class ScheduleState(StatesGroup):
    act = State()
    weekday = State()
    lesson = State()
    subject_name = State()
    id_name_lastname_username = State()
    group = State()


class OneDay(StatesGroup):
    weekday = State()


# ------ Начало проверки или изменения расписания ------
# @dp.message_handler(commands=["расписание"])
async def schedule(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=keyboard.schedule)


# @dp.callback_query_handler(text="Check_one_day")
async def check_one_day(callback: types.CallbackQuery):
    await OneDay.weekday.set()
    await callback.message.answer("Выберите день:", reply_markup=keyboard.change_s)
    await callback.answer()


# @dp.callback_query_handler(state=OneDay.weekday)
async def check_one_day_2(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(weekday=callback.data)
    a = ReplyKeyboardRemove()
    tg_id = callback.from_user.id
    group = ex_group(tg_id)
    data = await state.get_data()
    day = None
    even = None
    if data['weekday'] == "em" or data['weekday'] == "um":
        day = "Понедельник"
    elif data['weekday'] == "et" or data['weekday'] == "ut":
        day = "Вторник"
    elif data['weekday'] == "ew" or data['weekday'] == "uw":
        day = "Среда"
    elif data['weekday'] == "eth" or data['weekday'] == "uth":
        day = "Четверг"
    elif data['weekday'] == "ef" or data['weekday'] == "uf":
        day = "Пятница"
    elif data['weekday'] == "es" or data['weekday'] == "us":
        day = "Суббота"
    if data['weekday'][0] == "e":
        even = True
    elif data['weekday'][0] == "u":
        even = False
    row = []
    for i in range(1, 7):
        lesson = db_check(group, even, day, i)
        if lesson == "None":
            row.append(""" --- """)
        else:
            row.append(lesson[0])
    await callback.message.answer(
        f"{day}:\n\t8:00-9:30 {row[0]}\n\t9:40-11:10 {row[1]}\n\t11:45-13:15 {row[2]}\n\t13:50-15:20 {row[3]}\n\t15:30-17:00 {row[4]}\n\t17:10-18:40 {row[5]}",
        reply_markup=a)
    await callback.answer("Schedule checked!")
    await state.finish()


# ------ Начало проверки расписания ------
# @dp.callback_query_handler(text="Check_schedule")
async def check_schedule(callback: types.CallbackQuery):
    a = ReplyKeyboardRemove()
    group = ex_group(callback.from_user.id)
    is_even = True
    await callback.message.answer("Чётная неделя:")
    for day in weekdays:
        row = []
        for i in range(1, 7):
            lesson = db_check(group, is_even, day, i)
            if lesson == "None":
                row.append("-")
            else:
                row.append(lesson[0])
        await callback.message.answer(
            f"{day}:\n\t8:00-9:30 {row[0]}\n\t9:40-11:10 {row[1]}\n\t11:45-13:15 {row[2]}\n\t13:50-15:20 {row[3]}\n\t15:30-17:00 {row[4]}\n\t17:10-18:40 {row[5]}",
            reply_markup=a)
    is_even = False
    await callback.message.answer("Нечётная неделя:")
    for day in weekdays:
        row = []
        for i in range(1, 7):
            lesson = db_check(group, is_even, day, i)
            if lesson == "None":
                row.append("-")
            else:
                row.append(lesson[0])
        await callback.message.answer(
            f"{day}:\n\t8:00-9:30 {row[0]}\n\t9:40-11:10 {row[1]}\n\t11:45-13:15 {row[2]}\n\t13:50-15:20 {row[3]}\n\t15:30-17:00 {row[4]}\n\t17:10-18:40 {row[5]}",
            reply_markup=a)
    await callback.message.answer("Ваше расписание!")
    await callback.answer("Schedule checked!")


# ------ Начало введения изменений ------
# @dp.callback_query_handler(text="Changes")
async def which_changes(callback: types.CallbackQuery):
    await callback.message.answer("Что именно?", reply_markup=keyboard.change_w)
    await ScheduleState.act.set()
    await callback.answer()


# @dp.callback_query_handler(state=ScheduleState.act)
async def set_changes_to(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "Cancel":
        await state.finish()
        await callback.message.answer("Ok!")
        await callback.answer("Canceled!")
    else:
        await state.update_data(action=callback.data)
        await callback.answer("Changes type added!")
        await callback.message.answer("Какой день недели менять:", reply_markup=keyboard.change_s)
        await ScheduleState.weekday.set()
        await callback.answer()


# @dp.callback_query_handler(state=ScheduleState.weekday)
async def set_changes_to_weekday(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "Cancel":
        await state.finish()
        await callback.message.answer("Ok!")
        await callback.answer("Canceled!")
    else:
        await state.update_data(weekday=callback.data)
        await callback.answer("Weekday added!")
        await callback.message.answer("Какой предмет поменять:", reply_markup=keyboard.lesson)
        await ScheduleState.lesson.set()
        await callback.answer()


# @dp.callback_query_handler(state=ScheduleState.lesson)
async def set_changes_to_lesson(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "Cancel":
        await state.finish()
        await callback.message.answer("Ok!")
        await callback.answer("Canceled!")
    else:
        await state.update_data(lesson=callback.data)
        await callback.answer("Lesson chosen!")
        await callback.message.answer("""Напишите какой предмет добавить!\nИли же вы можете удалить написав "_" """)
        await ScheduleState.subject_name.set()
        await callback.answer()


# @dp.message_handler(state=ScheduleState.subject_name)
async def set_changes_to_subj(message: types.Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await message.answer("Записываю изменения.")
    data = await state.get_data()
    group = ex_group(message.from_user.id)
    day = None
    even = None
    if data['weekday'] == "em" or data['weekday'] == "um":
        day = "Понедельник"
    elif data['weekday'] == "et" or data['weekday'] == "ut":
        day = "Вторник"
    elif data['weekday'] == "ew" or data['weekday'] == "uw":
        day = "Среда"
    elif data['weekday'] == "eth" or data['weekday'] == "uth":
        day = "Четверг"
    elif data['weekday'] == "ef" or data['weekday'] == "uf":
        day = "Пятница"
    elif data['weekday'] == "es" or data['weekday'] == "us":
        day = "Суббота"
    if data['weekday'][0] == "e":
        even = True
    elif data['weekday'][0] == "u":
        even = False
    lesson = int(data['lesson'])
    subject = data['subject']
    if data["subject"] == "_":
        db_del_lesson(group, day, even, lesson)
        await message.answer("Удалил!")
    else:
        db_add_lesson(group, day, even, lesson, subject)
        await message.answer("Добавил!")
    await state.finish()


def register_handlers_schedule_f(dp: Dispatcher):
    dp.register_message_handler(schedule, commands=["schedule"])
    dp.register_callback_query_handler(check_one_day, text="Check_one_day")
    dp.register_callback_query_handler(check_one_day_2, state=OneDay.weekday)
    dp.register_callback_query_handler(check_schedule, text="Check_schedule")
    dp.register_callback_query_handler(which_changes, text="Changes")
    dp.register_callback_query_handler(set_changes_to, state=ScheduleState.act)
    dp.register_callback_query_handler(set_changes_to_weekday, state=ScheduleState.weekday)
    dp.register_callback_query_handler(set_changes_to_lesson, state=ScheduleState.lesson)
    dp.register_message_handler(set_changes_to_subj, state=ScheduleState.subject_name)
