from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from services.models import Employee


# async def check_employee(f_name, l_name, telegram_id):
#     tmp_user = Employee(f_name, l_name, telegram_id)
#     check = tmp_user.get_info_of_employee()
#     if check is None:
#         return False
#     elif check is []:
#         return True


async def cmd_start(message: types.Message):
    try:
        await message.answer(f"""Hello, <b>{message.from_user.full_name}</b> \n
                            Your first name: <b>{message.from_user.first_name}</b> \n
                            Your last name: <b>{message.from_user.last_name}</b> \n
                            Your id: <b>{message.from_user.id}</b>""", parse_mode='HTML')

        tmp_user = Employee(f_name=message.from_user.first_name, l_name=message.from_user.last_name,
                            telegram_id=message.from_user.id)
        a = tmp_user.get_info_of_employee()

        if a is None:
            print(f'1:: {tmp_user.get_info_of_employee }')
            await message.answer(f'I think you are not added to the our Base. Add?')
        elif a is not None:
            print(f'2:: {tmp_user.get_info_of_employee }')
            await message.answer(f'Welcome {message.from_user.full_name}')
    except Exception as _ex:
        await message.delete()
        await message.answer(f'Something happen: {_ex}')


async def add_me_cmd(message: types.Message):
    try:
        tmp_user = Employee(f_name=message.from_user.first_name, l_name=message.from_user.last_name,
                            telegram_id=message.from_user.id)
        res = tmp_user.add_employee()
        if res is False:
            await message.answer(f'You are not added. Maybe you are already registered')
        elif res is True:
            await message.answer(f"""Congratulations, {message.from_user.first_name} 
                                {message.from_user.last_name}! You are added""")
    except Exception as _ex:
        await message.delete()
        await message.answer(f'Something happen: {_ex}')


async def add_w_table_init_state(message: types.Message):
    await message.reply(f'Write the working day in format: 26.10.1994')
    # TODO: finish writing

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(add_me_cmd, commands=['add'])
