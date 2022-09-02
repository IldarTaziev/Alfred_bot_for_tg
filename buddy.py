import logging

from aiogram.utils.executor import start_webhook
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

import conf
from conf import conn, cursor
from conf import dp, bot
import asyncio
from db_f import ex_users
from datetime import time, date, datetime

import schedule
from threading import Thread


async def schedule_checker():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


def morning_schedule():
    users = ex_users()
    for user in users:
        return bot.send_message(user[0], "This is a message to send.")


# ------ функция начала работы -------
async def on_startup(dispatcher):
    now = datetime.now()
    await bot.set_webhook(conf.WEBHOOK_URL, drop_pending_updates=True)
    await bot.send_message("870284554", "On a board!")
    await bot.send_message("870284554", [now.time()])


# ------ функция окончания работы ------
async def on_shutdown(dispatcher):
    await bot.send_message("870284554", "Shutting down!")
    await bot.delete_webhook()
    cursor.close()
    conn.close()


from ls import start, default, schedule_f, weather, other

start.register_handlers_start(dp)
default.register_handlers_default(dp)
schedule_f.register_handlers_schedule_f(dp)
weather.register_handlers_weather(dp)
other.register_handlers_other(dp)

# ------ Не трогать! Это для правильной работы вебхуков! ------
if __name__ == '__main__':
    # Create the job in schedule.
    schedule.every().day.at("12:10").do(morning_schedule)

    # Spin up a thread to run the schedule check so it doesn't block your bot.
    # This will take the function schedule_checker which will check every second
    # to see if the scheduled job needs to be ran.
    Thread(target=schedule_checker).start()

    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=conf.WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=conf.WEBAPP_HOST,
        port=conf.WEBAPP_PORT,
    )
