import os
import bot
from aiogram import types


def auth(func):
    async def _wrapper(message: types.Message):
        print(os.getenv('BOT_ADMIN_ID'))
        print(message.from_user.id)
        if int(message.from_user.id) != int(os.getenv('BOT_ADMIN_ID')):
            return await message.answer(
                text=f"""<b>Sorry. You don\'t have access to this bot. </b>
                <b>Write to admin:</b>
                <a href="tg://user?id={os.getenv('BOT_ADMIN_ID')}">Dmitry Stepanov</a>""",
                parse_mode='HTML'
            )

        return await func(message)

    return _wrapper
