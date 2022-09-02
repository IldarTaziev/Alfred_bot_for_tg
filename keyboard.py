from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
w = KeyboardButton("/weather")
r = KeyboardButton("/ситуация_на_дароге")
l = KeyboardButton("/schedule")
menu.add(w).add(r).add(l)


weather = InlineKeyboardMarkup(row_width=1)
url_1 = InlineKeyboardButton(text='Yandex.Weather', url="https://yandex.ru/pogoda/")
url_2 = InlineKeyboardButton(text="GISMETEO", url="https://www.accuweather.com/")
url_3 = InlineKeyboardButton(text="Accuweather", url="https://www.gismeteo.ru/")
weather.add(url_1).add(url_2).add(url_3)


schedule = InlineKeyboardMarkup(row_width=1)
act_1 = InlineKeyboardButton(text='Изменить', callback_data="Changes")
act_2 = InlineKeyboardButton(text="Полностью", callback_data="Check_schedule")
act_3 = InlineKeyboardButton(text="Один день", callback_data="Check_one_day")
act_4 = InlineKeyboardButton(text="Отмена", callback_data="Cancel")
schedule.add(act_1).add(act_2).add(act_3).add(act_4)

change_w = InlineKeyboardMarkup(row_width=1)
replace = InlineKeyboardButton(text="Добавить/Изменить/Удалить", callback_data="re")
cancel = InlineKeyboardButton(text="Отмена", callback_data="Cancel")
change_w.add(replace).add(cancel)

change_s = InlineKeyboardMarkup(row_width=2)
em = InlineKeyboardButton(text='Пн Чет', callback_data="em")
um = InlineKeyboardButton(text='Пн Нечет', callback_data="um")
et = InlineKeyboardButton(text='Вт Чет', callback_data="et")
ut = InlineKeyboardButton(text='Вт Нечет', callback_data="ut")
ew = InlineKeyboardButton(text='Ср Чет', callback_data="ew")
uw = InlineKeyboardButton(text='Ср Нечет', callback_data="uw")
eth = InlineKeyboardButton(text='Чт Чет', callback_data="eth")
uth = InlineKeyboardButton(text='Чт Нечет', callback_data="uth")
ef = InlineKeyboardButton(text='Пт Чет', callback_data="ef")
uf = InlineKeyboardButton(text='Пт Нечет', callback_data="uf")
es = InlineKeyboardButton(text='Сб Чет', callback_data="es")
us = InlineKeyboardButton(text='Сб Нечет', callback_data="us")
ca = InlineKeyboardButton(text="Отмена", callback_data="Cancel")
change_s.row(em, um).row(et, ut).row(ew, uw).row(eth, uth).row(ef, uf).row(es, us).add(cancel)

lesson = InlineKeyboardMarkup(row_width=1)
l_1 = InlineKeyboardButton(text='Первая пара', callback_data="1")
l_2 = InlineKeyboardButton(text='Вторая пара', callback_data="2")
l_3 = InlineKeyboardButton(text='Третья пара', callback_data="3")
l_4 = InlineKeyboardButton(text='Четвертая пара', callback_data="4")
l_5 = InlineKeyboardButton(text='Пятая пара', callback_data="5")
l_6 = InlineKeyboardButton(text='Шестая пара', callback_data="6")
can = InlineKeyboardButton(text="Отмена", callback_data="Cancel")
lesson.add(l_1).add(l_2).add(l_3).add(l_4).add(l_5).add(l_6).add(can)