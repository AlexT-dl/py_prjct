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

name_list = ['Ketra\'s Chief Brakki','Varka\'s Chief Horus', 'Ember', 'Ketra\'s Commander Tayr', 'Varka\'s Commander Mos', 'Anakim', 'Ketra\'s Hero Hekaton', 'Lilith', 'Varka\'s Hero Shadith', 'Cherub Galaxia', 'Longhorn Golkonda', 'Fire of Wrath Shuriel', 'Hestia,Guardian Deity of the Hot Springs', 'Last Lesser Giant Glaki', 'Ocean Flame Ashakiel', 'Bloody Empress Decarbia', 'Death Lord Ipos', 'Death Lord Shax', 'Kernon', 'Last Lesser Giant Olkuth', 'Palatanos of Horrific Power', 'Storm Winged Naga', 'Antharas Priest Cloe', 'Krokian Padisha Sobekk', 'Death Lord Hallate', 'Doom Blade Tanatos', 'Vanor Chief Kandra', 'Water Dragon Seer Sheshark', 'Eilhalder von Hellmann', 'Immortal Savior Mardil', 'Flame of Splendor Barakiel']
url = "https://l2play.su/stat/raid/s1"

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!\nКоманды бота:\n/stat - показать список живых рб")


# Запуск процесса поллинга новых апдейтов
async def main():
    task1 = asyncio.create_task(dp.start_polling(bot))
    task2 = asyncio.create_task(status_perm())

    await asyncio.gather(task1, task2)


async def status_perm():
    while True:
        try:
            st_connection = sqlite3.connect('my_database.db')
            st_cursor = st_connection.cursor()
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            for parent in soup.find_all('tr'):
                items = parent.find_all('td')
                for item in items:
                    if (item.get_text() in name_list):
                        st_from_site = items[3].get_text()
                        rb_name = items[1].get_text()
                        st_cursor.execute('SELECT status FROM rb WHERE name = ?', (rb_name,))
                        st_from_db = str(st_cursor.fetchone())
                        st_from_db_cl = st_from_db.strip("(),\'")
                        if str(st_from_site) != st_from_db_cl:
                            st_cursor.execute('UPDATE rb SET status = ? where name = ?', (st_from_site, rb_name))
                            st_connection.commit()
                            '''await bot.send_message(495911930, (rb_name + ' - ' + st_from_site))'''
                            if str(st_from_site) == "Жив":
                                await bot.send_message(-1002481339545, (rb_name + ' - ' + st_from_site))
                            else:
                                await bot.send_message(-1002481339545, ('Убит ' + rb_name))
            st_connection.close()
            await asyncio.sleep(30)
        except:
            await asyncio.sleep(10)


@dp.message(Command("stat"))
async def stat(message):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        lst = []
        for parent in soup.find_all('tr'):
            items = parent.find_all('td')
            for item in items:
                if (item.get_text() in name_list):
                    j = items[3].get_text()
                    if j == 'Жив':
                        k = items[1].get_text()
                        lst.append(str(k))
                        frmtd_lst = '\n'.join(lst)
        '''await bot.send_message(495911930, frmtd_lst)'''
        await bot.send_message(-1002481339545, frmtd_lst)
    except ConnectionError as e:
        await bot.send_message(-1002481339545, e)


if __name__ == "__main__":
    asyncio.run(main())