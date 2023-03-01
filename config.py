from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


token = '5929588021:AAH-mIshbX49EBK0NAQND1DHeizTcI2a2vY'
dictionary = 'https://telegra.ph/Slovar-slenga-02-03'
ID = 974923385
storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)