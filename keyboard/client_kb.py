from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('Помощь')
b2 = KeyboardButton('Слово')
b3 = KeyboardButton('Список слов')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

kb_client.add(b1).add(b2).insert(b3)