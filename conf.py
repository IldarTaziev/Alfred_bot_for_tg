import os
import psycopg2 as ps
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher


# ------ базовые неизменные значения ------
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
API_Weather = os.getenv('API_WEATHER')
TOKEN = os.getenv('BOT_TOKEN')


weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
memory = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=memory)


conn = ps.connect(os.getenv("DATABASE_URL"))
cursor = conn.cursor()


# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'