from aiogram import types, Dispatcher
from config import bot, dictionary
from keyboard import kb_client
from data_base import sqlite_db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text


class FSMclient(StatesGroup):
    word = State()


async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Что хотите узнать?', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Напишите боту в лс')


async def send_definition_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Введите слово')
    await FSMclient.word.set()


async def load_word(message: types.Message, state: FSMContext):
    word = message.text
    await sqlite_db.sql_send_def(message, word)
    await state.finish()


async def send_dict_command(message: types.Message):
    await bot.send_message(message.from_user.id, dictionary)


async def send_help_command(message: types.Message):
    help = '*100+ сленговых слов и фраз!* \n\n' \
           'Доступные команды: \n' \
           '*Начать* - запустить бота \n' \
           '*Слово* - ввести слово \n' \
           '*Список слов* - открыть список слов'
    await bot.send_message(message.from_user.id, help, parse_mode="Markdown")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(commands_start, Text(startswith=['Начать', 'start', 'help'], ignore_case=True))
    dp.register_message_handler(load_word, state=FSMclient.word)
    dp.register_message_handler(send_definition_command, Text(contains='Слово', ignore_case=True), state=None)
    dp.register_message_handler(send_dict_command, Text(contains='Список слов', ignore_case=True))
    dp.register_message_handler(send_help_command, Text(contains='Помощь', ignore_case=True))
