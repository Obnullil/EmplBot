import sys

from bot import handlers, keyboards
from bot.init_bot import dp

from aiogram.utils import executor
from bot.handlers import client
from bot.init_bot import dp


async def on_startup(_):
    print('Bot is run')


if __name__ == '__main__':
    client.register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)