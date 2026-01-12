import requests
from bs4 import BeautifulSoup

url = "https://l2play.su/stat/raid/s1"

name_list = ['Ketra\'s Chief Brakki','Varka\'s Chief Horus', 'Ember', 'Ketra\'s Commander Tayr', 'Varka\'s Commander Mos', 'Anakim', 'Ketra\'s Hero Hekaton', 'Lilith', 'Varka\'s Hero Shadith', 'Cherub Galaxia', 'Longhorn Golkonda', 'Fire of Wrath Shuriel', 'Hestia,Guardian Deity of the Hot Springs', 'Last Lesser Giant Glaki', 'Ocean Flame Ashakiel', 'Bloody Empress Decarbia', 'Death Lord Ipos', 'Death Lord Shax', 'Kernon', 'Last Lesser Giant Olkuth', 'Palatanos of Horrific Power', 'Storm Winged Naga', 'Antharas Priest Cloe', 'Krokian Padisha Sobekk', 'Death Lord Hallate', 'Doom Blade Tanatos', 'Vanor Chief Kandra', 'Water Dragon Seer Sheshark', 'Eilhalder von Hellmann', 'Immortal Savior Mardil']

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")


'''всё в функцию и сразу сравнялка бд с итемс 0 3'''
for parent in soup.find_all('tr'):
    items = parent.find_all('td')
    for item in items:
        if (item.get_text() in name_list):
            j = items[3].get_text()
            if j == 'Жив':
                k = items[1].get_text()
                l = items[3].get_text()
                print(k, l)
