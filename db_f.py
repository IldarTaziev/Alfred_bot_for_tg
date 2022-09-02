from conf import conn, cursor


# ------ Добавление нового рассписания ------
def db_add_new_schedule(group: str):
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS public."{group}"
(
    "Weekday" text COLLATE pg_catalog."default" NOT NULL,
    "Is_even" boolean NOT NULL,
    "Lesson_1" text COLLATE pg_catalog."default",
    "Lesson_2" text COLLATE pg_catalog."default",
    "Lesson_3" text COLLATE pg_catalog."default",
    "Lesson_4" text COLLATE pg_catalog."default",
    "Lesson_5" text COLLATE pg_catalog."default",
    "Lesson_6" text COLLATE pg_catalog."default",
    CONSTRAINT "{group}_pkey" PRIMARY KEY ("Weekday")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."{group}"
    OWNER to inzjbrdnrulmmz;""")
    conn.commit()


def db_add_weekdays(weekdays: list):
    is_even = True
    for day in weekdays:
        cursor.execute(
            f"""INSERT INTO public."1IS02"(
     "Weekday", "Is_even"
    VALUES ('{day}'::text, {is_even}::boolean);""", )
        conn.commit()
    is_even = False
    for day in weekdays:
        cursor.execute(
            f"""INSERT INTO public."1IS02"(
         "Weekday", "Is_even"
        VALUES ('{day}'::text, {is_even}::boolean);""", )
        conn.commit()


# ------ Добавление нового пользователя в базу данных ------
def db_add_user(tg_id: str, name: str, lastname: str, username: str, group: str):
    cursor.execute(
        f"""INSERT INTO public."Users" (
"ID", "Name", "LastName", "Username", "Group") VALUES (
'{tg_id}'::integer, '{name}'::text, '{lastname}'::text, '{username}'::text, '{group}'::text)
 returning "Name";""")
    conn.commit()


# ------ ------
def ex_users():
    cursor.execute(
        f"""SELECT "ID"
                FROM public."Users";""")
    users = cursor.fetchall()
    return users


def ex_group(tg_id: str):
    cursor.execute(
        f"""SELECT "Group" FROM public."Users" WHERE "ID"='{tg_id}';""")
    group = cursor.fetchone()
    return group[0]


# ------ Добавление новой пары в расписание ------
def db_add_lesson(group: str, weekday: str, is_even: bool, lesson: int, subject: str):
    cursor.execute(
        f"""UPDATE public."{group}" SET "Lesson_{lesson}" = '{subject}' WHERE "Weekday" = '{weekday}' AND "Is_even" = {is_even};""")
    conn.commit()


# ------ Удаление пары из расписания ------
def db_del_lesson(group: str, weekday: str, is_even: bool, lesson: int):
    cursor.execute(
        f"""UPDATE public."{group}" SET "Lesson_{lesson}" = NULL WHERE "Weekday" = '{weekday}' AND "Is_even" = {is_even};""")
    conn.commit()


# ------ Вывод расписания целиком ------
def db_check(group: str, is_even: bool, weekday: str, lesson: int):
    cursor.execute(
        f"""SELECT "Lesson_{lesson}"
                FROM public."{group}" WHERE "Is_even"={is_even} AND "Weekday"='{weekday}';""")
    lesson = cursor.fetchone()
    return lesson
