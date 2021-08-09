''' Создать парсер с бк конторы
Парсить 4 страницы сайта - Киберспорт, Футбол, Баскетбол, Теннис
с каждого матча получать значение в тегах:
                                            1. Время (17:00 < time.now() < 20:00)
                                            2. Команды
                                            3. Коэфициенты на победу > 1.8      '''

import requests
from bs4 import BeautifulSoup
from datetime import date


class Bets:
    def __init__(self, url):
        self.url = url
        self.bet_list = []
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'lxml')
        self.matches = self.soup.find_all('div', class_='c-events__item c-events__item_game')

    # 'https://1xstavka.ru/line/Football/'
    # 'https://1xstavka.ru/line/Basketball/'
    # 'https://1xstavka.ru/line/Esports/'
    # 'https://1xstavka.ru/line/Tennis/'

    def find_matches(self):

        url = self.url

        def get_title(str_match):
            title = (str_match.find('span', class_='n')).get('title')
            if not '(' in title:
                return title

        def get_date(str_match, url=None):
            if url == 'https://1xstavka.ru/line/Tennis/':
                pass
            else:
                return (str_match.find('span')).text

        def get_winners(str_match):
            return ((str_match.find_all('span', class_='c-bets__inner'))[0].text,
                    (str_match.find_all('span', class_='c-bets__inner'))[2].text)

        for match in self.matches:
            title = get_title(match)
            match_date = get_date(match, url)
            winners = get_winners(match)
            temporary_tuple = (title, match_date, winners)
            self.bet_list.append(temporary_tuple)
        for i, k, j in self.bet_list:
            print(i, k, j)


bet = Bets('https://1xstavka.ru/line/Esports/').find_matches()
