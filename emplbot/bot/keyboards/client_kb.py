from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Add Employee')
b2 = KeyboardButton('New business day record')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.row(b2)
