''' Создать парсер с бк конторы
Парсить 4 страницы сайта - Киберспорт, Футбол, Баскетбол, Теннис
с каждого матча получать значение в тегах:
                                            1. Время (17:00 < time.now() < 20:00)
                                            2. Команды
                                            3. Коэфициенты на победу > 1.8      '''

import requests
from bs4 import BeautifulSoup
from datetime import *
import time
import schedule
import sqlite3


# 'https://1xstavka.ru/line/Football/'
# 'https://1xstavka.ru/line/Basketball/'
# 'https://1xstavka.ru/line/Esports/'
# 'https://1xstavka.ru/line/Tennis/'

def find_matches(url, sport_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    matches = soup.find_all('div', class_='c-events__item c-events__item_game')
    bet_list = []

    def get_title(str_match):
        title = (str_match.find('span', class_='n')).get('title')
        if not '(' in title:
            return title.strip()

    def get_date(str_match, url=None):
        if url == 'https://1xstavka.ru/line/Tennis/':
            pass
        else:
            return (str_match.find('span')).text

    def get_winners(str_match):
        return ((str_match.find_all('span', class_='c-bets__inner'))[0].text,
                (str_match.find_all('span', class_='c-bets__inner'))[2].text)

    for match in matches:
        title = get_title(match)
        match_date = get_date(match, url)
        winners = get_winners(match)
        temporary_tuple = (title, match_date, winners)
        bet_list.append(temporary_tuple)
    for title, inc_date, winnerq in bet_list:
        if title is None:
            continue
        bet_date, bet_time = inc_date.split(' ')[0] + '.2021', inc_date.split(' ')[1]
        bet_date_obj = datetime.strptime(bet_date, '%d.%m.%Y').date()
        if date.today() <= bet_date_obj <= (date.today() + timedelta(days=1)):
            max_coef = str(winnerq[0] + ' Победа первого') if (float(winnerq[0]) >= 1.75) else str(winnerq[1] + ' Победа второго')
            if sport_name == 'Football':
                conn = sqlite3.connect('bot_DB.db')
                cur = conn.cursor()
                cur.execute("INSERT INTO football(title, date, winner) VALUES (?, ?, ?)", (title, inc_date, max_coef))
                conn.commit()
                conn.close()
            elif sport_name == 'Esports':
                conn = sqlite3.connect('bot_DB.db')
                cur = conn.cursor()
                cur.execute("INSERT INTO esports(title, date, winner) VALUES (?, ?, ?)", (title, inc_date, max_coef))
                conn.commit()
                conn.close()


schedule.every(1).seconds.do(find_matches, 'https://1xstavka.ru/line/Football/', 'Football')
schedule.every(1).seconds.do(find_matches, 'https://1xstavka.ru/line/Esports/', 'Esports')
# schedule.every(10).seconds.do(find_matches, 'https://1xstavka.ru/line/Esports/')
# schedule.every(10).seconds.do(find_matches, 'https://1xstavka.ru/line/Tennis/')

while True:
    schedule.run_pending()
    time.sleep(1)
