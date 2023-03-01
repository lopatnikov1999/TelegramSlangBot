import config
from data_base import sqlite_db
from aiogram.utils import executor

async def on_startup(_):
    print('Bot is running')
    sqlite_db.sql_start()

from handlers import client, admin

client.register_handlers_client(config.dp)
admin.register_handlers_admin(config.dp)


executor.start_polling(config.dp, skip_updates=True, on_startup=on_startup)