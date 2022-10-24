import asyncio
import logging

from bot.config_bot import config
print('1')
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token="5735379123:AAEjj0K7saEZu5iupM8wHUsOsAXXqf1qSZI")
dp = Dispatcher(bot, storage=MemoryStorage())
