import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import requests
from bs4 import BeautifulSoup


# Объект бота
bot = Bot(token="7878418002:AAHdRMUw-eHF3QZEwbu72McbO-fHMRVRQfI")
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!\nКоманды бота:\n/showlist - показать список постоянно отслеживаемых персонажей\n/add -"
                         " добавить персонажа в список для отслеживания\n/remove - удалить"
                         " персонажа из списка\n/clear - очистить список\nДля того чтобы проверить онлайн ли персонаж, "
                         "просто введите его имя в чат")


@dp.message(Command("add"))
async def add_func(message):
    ad_name = message.text
    ad_name_stripped = ad_name[5:]
    ad_connection = sqlite3.connect('listnames.db')
    ad_cursor = ad_connection.cursor()
    ad_cursor.execute("INSERT INTO Names (name) VALUES (?)", (ad_name_stripped,))
    ad_connection.commit()
    ad_connection.close()
    await bot.send_message(495911930, (ad_name_stripped + ' добавлен в список Online'))


@dp.message(Command("addo"))
async def addo_func(message):
    ado_name = message.text
    ado_name_stripped = ado_name[6:]
    ado_connection = sqlite3.connect('listnames.db')
    ado_cursor = ado_connection.cursor()
    ado_cursor.execute("INSERT INTO ONames (name) VALUES (?)", (ado_name_stripped,))
    ado_connection.commit()
    ado_connection.close()
    await bot.send_message(495911930, (ado_name_stripped + ' добавлен в список Offline'))


@dp.message(Command("remove"))
async def rmv_func(message):
    rmv_name = message.text
    rmv_name_stripped = rmv_name[8:]
    rmv_connection = sqlite3.connect('listnames.db')
    rmv_cursor = rmv_connection.cursor()
    rmv_cursor.execute("DELETE FROM Names WHERE name = (?)", (rmv_name_stripped,))
    rmv_connection.commit()
    rmv_connection.close()
    await bot.send_message(495911930, (rmv_name_stripped + ' удален из списка Online'))


@dp.message(Command("removeo"))
async def rmvo_func(message):
    rmvo_name = message.text
    rmvo_name_stripped = rmvo_name[9:]
    rmvo_connection = sqlite3.connect('listnames.db')
    rmvo_cursor = rmvo_connection.cursor()
    rmvo_cursor.execute("DELETE FROM ONames WHERE name = (?)", (rmvo_name_stripped,))
    rmvo_connection.commit()
    rmvo_connection.close()
    await bot.send_message(495911930, (rmvo_name_stripped + ' удален из списка Offline'))


@dp.message(Command("clear"))
async def clr_func(message):
    clr_connection = sqlite3.connect('listnames.db')
    clr_cursor = clr_connection.cursor()
    clr_cursor.execute("DELETE FROM Names")
    clr_connection.commit()
    clr_connection.close()
    await bot.send_message(495911930, 'Очищен список ONline')


@dp.message(Command("clearo"))
async def clr_func(message):
    clro_connection = sqlite3.connect('listnames.db')
    clro_cursor = clro_connection.cursor()
    clro_cursor.execute("DELETE FROM ONames")
    clro_connection.commit()
    clro_connection.close()
    await bot.send_message(495911930, 'Очищен список OFFline')


@dp.message(Command("showlist"))
async def show_func(message):
    sl_connection = sqlite3.connect('listnames.db')
    sl_cursor = sl_connection.cursor()
    sl_cursor.execute('''SELECT name FROM Names
            ''')
    sl_name = sl_cursor.fetchall()
    sl_lst = []
    for j in sl_name:
        sl_a = ' '.join(j)
        sl_lst.append(sl_a)
    sl_connection.commit()
    sl_connection.close()
    await bot.send_message(495911930, (', '.join(sl_lst) + '!'))


@dp.message(Command("showlisto"))
async def show_func(message):
    slo_connection = sqlite3.connect('listnames.db')
    slo_cursor = slo_connection.cursor()
    slo_cursor.execute('''SELECT name FROM ONames
            ''')
    slo_name = slo_cursor.fetchall()
    slo_lst = []
    for j in slo_name:
        slo_a = ' '.join(j)
        slo_lst.append(slo_a)
    slo_connection.commit()
    slo_connection.close()
    await bot.send_message(495911930, (', '.join(slo_lst) + '!'))


@dp.message()
async def echo_check(message):
    ec_name = message.text
    try:
        ec_page = requests.get('https://draconic.ru/onlinelist/')
    except ConnectionError:
        await bot.send_message(495911930, 'Нет коннекта к сайту')
    ec_soup = BeautifulSoup(ec_page.text, 'html.parser')
    ec_list = ec_soup.find('body').text
    if ec_name in ec_list:
        await bot.send_message(495911930, (ec_name + ' is Online'))
    else:
        await bot.send_message(495911930, (ec_name + ' is Off'))


@dp.message()
async def echo_check(message):
    await bot.send_message(495911930, (message.text))


# Запуск процесса поллинга новых апдейтов
async def main():
    task1 = asyncio.create_task(dp.start_polling(bot))
    task2 = asyncio.create_task(onl_perm())

    await asyncio.gather(task1, task2)


async def onl_perm():
    while True:
        await asyncio.sleep(30)
        op_connection = sqlite3.connect('listnames.db')
        op_cursor = op_connection.cursor()
        op_cursor.execute('''SELECT name FROM Names
        ''')
        op_name = op_cursor.fetchall()
        op_lst = []
        for op_i in op_name:
            op_a = ' '.join(op_i)
            op_lst.append(op_a)
        op_connection.commit()
        op_connection.close()
        try:
            op_page = requests.get('https://draconic.ru/onlinelist/')
        except ConnectionError:
            await bot.send_message(495911930, 'Нет коннекта к сайту')
        op_soup = BeautifulSoup(op_page.text, 'html.parser')
        for op_j in op_lst:
            op_list = op_soup.find('body').text
            if op_j in op_list:
                pass
            else:
                await bot.send_message(495911930, (op_j + ' is OFFLINE'))


async def ofl_perm():
    while True:
        await asyncio.sleep(30)
        ofp_connection = sqlite3.connect('listnames.db')
        ofp_cursor = ofp_connection.cursor()
        ofp_cursor.execute('''SELECT name FROM ONames
        ''')
        ofp_name = ofp_cursor.fetchall()
        ofp_lst = []
        for ofp_i in ofp_name:
            ofp_a = ' '.join(ofp_i)
            ofp_lst.append(ofp_a)
        ofp_connection.commit()
        ofp_connection.close()
        try:
            ofp_page = requests.get('https://draconic.ru/onlinelist/')
        except ConnectionError:
            await bot.send_message(495911930, 'Нет коннекта к сайту')
        ofp_soup = BeautifulSoup(ofp_page.text, 'html.parser')
        for ofp_j in ofp_lst:
            ofp_list = ofp_soup.find('body').text
            if ofp_j in ofp_list:
                await bot.send_message(495911930, (ofp_j + ' OFFLINE'))
            else:
                pass

if __name__ == "__main__":
    asyncio.run(main())
