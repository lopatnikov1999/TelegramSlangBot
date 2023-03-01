from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from config import bot, ID
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboard import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class FSMAdmin_load(StatesGroup):
    name = State()
    description = State()


class FSMAdmin_del(StatesGroup):
    name = State()


async def admin_command(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.from_user.id, 'Отправляем админскую панель',
                               reply_markup=admin_kb.button_case_admin)
        await message.delete()


async def load_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin_load.name.set()
        await message.reply('Введите слово, которое хотите добавить')


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Готово')


async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin_load.next()
        await message.reply('Введите определение')


async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text

        await sqlite_db.sql_add_command(state)
        await state.finish()


async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace("del ", ""))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалено')


async def delete_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin_del.name.set()
        await message.reply('Введите слово, которое хотите удалить')


async def delete_word(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        word_to_delete = message.text
        inline_kb = InlineKeyboardMarkup()
        inline_button = InlineKeyboardButton('Подтвердить', callback_data=f'del {word_to_delete}')
        inline_kb.add(inline_button)
        await bot.send_message(message.from_user.id, text=f'Удалить *{word_to_delete}*', reply_markup=inline_kb,
                               parse_mode="Markdown")
        await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(load_start, Text(startswith=['Загрузить'], ignore_case=True), state=None)
    dp.register_message_handler(cancel_handler, state='*', commands='Отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_name, state=FSMAdmin_load.name)
    dp.register_message_handler(load_description, state=FSMAdmin_load.description)
    dp.register_message_handler(admin_command, commands=['admin'])
    dp.register_message_handler(delete_start, Text(startswith=['Удалить'], ignore_case=True), state=None)
    dp.register_message_handler(delete_word, state=FSMAdmin_del.name)
    dp.register_callback_query_handler(del_callback_run, Text(startswith='del ', ignore_case=True))
