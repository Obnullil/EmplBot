import datetime
from datetime import datetime as dt

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from services.models import Employee
from bot.handlers.admin import auth


class FSMClient_reg_person(StatesGroup):
    st_in_system = State()


class FSMClient_w_table(FSMClient_reg_person, StatesGroup):
    st_in_system = State()
    st_w_day = State()
    st_w_city = State()
    st_name_project = State()
    st_descr_work = State()
    st_notes = State()
    st_start_shift = State()
    st_end_shift = State()
    st_view_rec_row = State()


# Command "Start": Init bot for new user or check the old user
@auth
async def cmd_start(message: types.Message):
    try:
        await message.answer(f"""Hello, <b>{message.from_user.full_name}</b> \n
                            Your first name: <b>{message.from_user.first_name}</b> \n
                            Your last name: <b>{message.from_user.last_name}</b> \n
                            Your id: <b>{message.from_user.id}</b>""", parse_mode='HTML')
        # Check the user data in database
        tmp_user = Employee(f_name=message.from_user.first_name, l_name=message.from_user.last_name,
                            telegram_id=message.from_user.id)
        user_info = tmp_user.get_info_of_employee()
        # if user_info is None - user don't have the data in Database; if user_info is [] - user exists
        if user_info is None:
            print(f'1:: {tmp_user.get_info_of_employee }')
            await message.answer(f'I think you are not added to the our Base. Add?')
        elif user_info is not None:
            print(f'2:: {tmp_user.get_info_of_employee }')
            await FSMClient_reg_person.st_in_system.set()
            await message.answer(f'Welcome {message.from_user.full_name}')
    except Exception as _ex:
        await message.delete()
        await message.answer(f'Something happen: {_ex}')


# add info about users in database (for new users)
@auth
async def add_me_cmd(message: types.Message):
    try:
        tmp_user = Employee(f_name=message.from_user.first_name, l_name=message.from_user.last_name,
                            telegram_id=message.from_user.id)
        res = tmp_user.add_employee()
        if res is False:
            await message.answer(f'You are not added. Maybe you are already registered')
        elif res is True:
            await FSMClient_reg_person.st_in_system.set()
            await message.answer(f"""Congratulations, {message.from_user.first_name} 
                                {message.from_user.last_name}! You are added""")
    except Exception as _ex:
        await message.delete()
        await message.answer(f'Something happen: {_ex}')


# Add work table (one work day) of the user in the Database
async def add_w_table_init_state(message: types.Message, state=FSMContext):
    await FSMClient_w_table.st_w_day.set()
    await message.reply(f'Write the working day in format: 26.10.1994')


async def w_day_entry(message: types.Message, state=FSMContext):
    try:
        tmp_message = dt.strptime(message.text, '%d.%m.%Y')
        async with state.proxy() as proxy_w_table_data:
            proxy_w_table_data['st_w_day'] = tmp_message
            await FSMClient_w_table.next()
            await message.reply(f'Write the city where you did the project')
            print(proxy_w_table_data)
    except Exception as _ex:
        print(f'[INFO] client/w_day_entry: {_ex}')
        await message.reply(f'You writed wrong format.Write the working day in format: 26.10.1994')


async def w_city_entry(message: types.Message, state=FSMContext):
    try:
        # TODO: Add validation for data (check the correct name of the city or country)
        async with state.proxy() as proxy_w_table_data:
            proxy_w_table_data['st_w_city'] = message.text
            await FSMClient_w_table.next()
            await message.reply(f'Write the name of project')
    except Exception as _ex:
        print(f'[INFO] client/w_city_entry: {_ex}')
        await message.reply(f"name is very long")


async def w_name_project(message: types.Message, state=FSMContext):
    try:
        # TODO: Add validation for data (check the long of string)
        async with state.proxy() as proxy_w_table_data:
            proxy_w_table_data['st_name_project'] = message.text
            await FSMClient_w_table.next()
            await message.reply(f'Write the description of the project if it\'s need')
    except Exception as _ex:
        print(f'[INFO] client/w_city_entry: {_ex}')
        await message.reply(f"name is very long")


async def w_descr_project(message: types.Message, state=FSMContext):
    try:
        # TODO: Add validation for data (check the long of string)
        async with state.proxy() as proxy_w_table_data:
            proxy_w_table_data['st_descr_work'] = message.text
            await FSMClient_w_table.next()
            await message.reply(f'Write the notes of the project if it\'s need')
    except Exception as _ex:
        print(f'[INFO] client/w_descr_project: {_ex}')
        await message.reply(f'name is very long')


async def w_notes(message: types.Message, state=FSMContext):
    try:
        # TODO: Add validation for data (check the long of string)
        async with state.proxy() as proxy_w_table_data:
            proxy_w_table_data['st_notes'] = message.text
            await FSMClient_w_table.next()
            await message.reply(f'Write the time when you shift is start. Format: 09:00')
    except Exception as _ex:
        print(f'[INFO] client/w_notes: {_ex}')
        await message.reply(f'name is very long')


async def w_start_shift(message: types.Message, state=FSMContext):
    try:
        tmp_message = dt.strptime(message.text, '%H:%M')
        async with state.proxy() as proxy_w_table_data:
            tmp_var_dt = datetime.datetime                                              # temp variable datetime

            start_shift_dt = tmp_var_dt.combine(proxy_w_table_data['st_w_day'].date(),  # data from st_w_day +
                                                tmp_message.time())                     # time when shift is finish

            proxy_w_table_data['st_start_shift'] = start_shift_dt
            await FSMClient_w_table.next()
            await message.reply(f'Write the time when you shift is finish. Format: 09:00')
            print(proxy_w_table_data)
    except Exception as _ex:
        print(f'[INFO] client/w_day_entry: {_ex}')
        await message.reply(f'You writed wrong format.Write the working day in format: 09:00')


async def w_end_shift(message: types.Message, state=FSMContext):
    try:
        tmp_message = dt.strptime(message.text, '%H:%M')
        async with state.proxy() as proxy_w_table_data:
            tmp_var_dt = datetime.datetime                                              # temp variable datetime

            end_shift_dt = tmp_var_dt.combine(proxy_w_table_data['st_w_day'].date(),    # data from st_w_day +
                                                tmp_message.time())                     # time when shift is finish

            proxy_w_table_data['st_end_shift'] = end_shift_dt
            # await FSMClient_w_table.next()
            await message.reply(f'WAIT')

            shift_time_difference = proxy_w_table_data['st_end_shift'] - proxy_w_table_data['st_start_shift']
            print(f'shift_time_difference: {shift_time_difference}')
            proxy_w_table_data['st_view_rec_row'] = shift_time_difference
            await message.bot.send_message(chat_id=message.chat.id, text=f"""
                            st_w_day = <b>{proxy_w_table_data['st_w_day']}</b>
                            st_w_city = <b>{proxy_w_table_data['st_w_city']}</b>
                            st_name_project = <b>{proxy_w_table_data['st_name_project']}</b>
                            st_descr_work = <b>{proxy_w_table_data['st_descr_work']}</b>
                            st_notes = <b>{proxy_w_table_data['st_notes']}</b>
                            st_start_shift = <b>{proxy_w_table_data['st_start_shift']}</b>
                            st_end_shift = <b>{proxy_w_table_data['st_end_shift']}</b>
                            st_view_rec_row = <b>{proxy_w_table_data['st_view_rec_row']}</b>
                        """, parse_mode='HTML')

            print(proxy_w_table_data)
    except Exception as _ex:
        print(f'[INFO] client/w_day_entry: {_ex}')
        await message.reply(f'You writed wrong format.Write the working day in format: 09:00')




def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(add_me_cmd, commands=['add'])
    dp.register_message_handler(add_w_table_init_state, commands=['add_w_table'], state=FSMClient_reg_person.st_in_system)
    dp.register_message_handler(w_day_entry, state=FSMClient_w_table.st_w_day)
    dp.register_message_handler(w_city_entry, state=FSMClient_w_table.st_w_city)
    dp.register_message_handler(w_name_project, state=FSMClient_w_table.st_name_project)
    dp.register_message_handler(w_descr_project, state=FSMClient_w_table.st_descr_work)
    dp.register_message_handler(w_notes, state=FSMClient_w_table.st_notes)
    dp.register_message_handler(w_start_shift, state=FSMClient_w_table.st_start_shift)
    dp.register_message_handler(w_end_shift, state=FSMClient_w_table.st_end_shift)
    # dp.register_message_handler(view_rec_row, state=FSMClient_w_table.st_view_rec_row)
