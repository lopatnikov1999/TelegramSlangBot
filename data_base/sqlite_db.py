import sqlite3 as sq
from config import bot


def to_up_first_letter(word):
    word = word[0].upper() + word[1:].lower()
    return word


def sql_start():
    global base, cur
    base = sq.connect('slang_dict.db')
    cur = base.cursor()
    if base:
        print('Data base connected')
    base.execute('CREATE TABLE IF NOT EXISTS dictionary(name TEXT PRIMARY KEY, description TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO dictionary VALUES (?, ?)', tuple(data.values()))
        base.commit()


# async def sql_read(message):
#     for ret in cur.execute('SELECT * FROM dictionary').fetchall():
#         await bot.send_message(message.from_user.id, f'*Слово:* {ret[0]}\n*Значение:* {ret[1]}',
#                                parse_mode="Markdown")


async def sql_delete_command(data):
    cur.execute('DELETE FROM dictionary WHERE name = ?', (data,))
    base.commit()


async def sql_read2():
    return cur.execute('SELECT * FROM dictionary').fetchall()


async def sql_send_def(message, word):
    c = True
    if c:
        word = word.upper()  # приводим к верхнему регистру все слово
        cur.execute('SELECT description FROM dictionary WHERE UPPER(name) = ?', (word,))
        desc = cur.fetchone() # извлекаем строку
        if desc:
            for ret in desc:
                await bot.send_message(message.from_user.id, f'*{word}* — {ret}', parse_mode="Markdown")
            return
        else:
            word = to_up_first_letter(word) # приводим к верхнему регистру первую букву
            cur.execute('SELECT description FROM dictionary WHERE name = ?', (word,))
            desc = cur.fetchone() # извлекаем строку
            if desc:
                for ret in desc:
                    await bot.send_message(message.from_user.id, f'*{word}* — {ret}', parse_mode="Markdown")
            else:
                c = False
    if not c:
        await bot.send_message(message.from_user.id, f'Слова *{word}* нет в словаре', parse_mode="Markdown")
