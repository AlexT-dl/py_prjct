import sqlite3

conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

name_list = ['Ketra\'s Chief Brakki','Varka\'s Chief Horus', 'Ember', 'Ketra\'s Commander Tayr', 'Varka\'s Commander Mos', 'Anakim', 'Ketra\'s Hero Hekaton', 'Lilith', 'Varka\'s Hero Shadith', 'Cherub Galaxia', 'Longhorn Golkonda', 'Fire of Wrath Shuriel', 'Hestia,Guardian Deity of the Hot Springs', 'Last Lesser Giant Glaki', 'Ocean Flame Ashakiel', 'Bloody Empress Decarbia', 'Death Lord Ipos', 'Death Lord Shax', 'Kernon', 'Last Lesser Giant Olkuth', 'Palatanos of Horrific Power', 'Storm Winged Naga', 'Antharas Priest Cloe', 'Krokian Padisha Sobekk', 'Death Lord Hallate', 'Doom Blade Tanatos', 'Vanor Chief Kandra', 'Water Dragon Seer Sheshark', 'Eilhalder von Hellmann', 'Immortal Savior Mardil']

# Создание таблицы (пример)
'''cursor.execute("update rb set status = 'Мертв'")
conn.commit()'''

cursor.execute('''select * from rb''')
for row in cursor.fetchall():
    print(row)

conn.commit()
conn.close()