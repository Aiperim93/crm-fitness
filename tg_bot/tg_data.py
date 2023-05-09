import logging
import os
import aiohttp
import redis
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from keyboards import kb, admin_kb
from aiogram.contrib.fsm_storage.memory import MemoryStorage

pool = redis.ConnectionPool(host='redis', port=6379, db=1)
redis_ = redis.Redis(connection_pool=pool)
TOKEN = os.environ.get('BOT_TOKEN')
API_TOKEN = os.environ.get('API_TOKEN')
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def get_admin():
    url: str = f"{os.environ.get('ADMIN')}"
    headers = {
        'Authorization': API_TOKEN
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            if response.status == 200:
                admin = (await response.json())
                return admin


async def start(message: types.Message):
    if message.from_user.id == await get_admin():
        await message.answer(text='Добро пожаловать!', reply_markup=admin_kb)
    else:
        await message.answer(text='Добро пожаловать!', reply_markup=kb)


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
