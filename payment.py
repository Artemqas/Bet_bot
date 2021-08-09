import requests
import json
import pyqiwi
from random import choice
from string import ascii_letters
from string import digits

from const import *

import sqlite3

def get_operations():
    ''' Добавление операций в таблицу '''
    api_access_token = '75659360669380c2c1a2df1b48e88beb' # токен можно получить здесь https://qiwi.com/api
    my_login = '+79777288083' # номер QIWI Кошелька в формате +79991112233

    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + api_access_token
    parameters = {'rows': '1'}
    h = s.get('https://edge.qiwi.com/payment-history/v1/persons/'+my_login+'/payments', params = parameters)

    conn = sqlite3.connect('bot_DB.db')
    cur = conn.cursor()

    for i in json.loads(h.text)['data']:
        sum_amount_get = i['sum']['amount']
        comment_get = i['comment']
        cur.execute("INSERT INTO PAYMENT(amount, comment) VALUES (?, ?)", (sum_amount_get, comment_get,))
        conn.commit()
    conn.close()


def create_comment():
    ''' Создание уникального комментария и добавления его в БД в таблицу COMMENTS'''
    conn = sqlite3.connect('bot_DB.db')
    created_comment = ''.join(choice(ascii_letters) + choice(digits) for i in range(4))
    cur = conn.cursor()
    cur.execute("INSERT INTO COMMENTS(comment) VALUES (?) ", (created_comment,))
    conn.commit()
    conn.close()
    return created_comment

def get_comment():
    ''' Возвращает последний созданный комментарий '''
    conn = sqlite3.connect('bot_DB.db')
    cur = conn.cursor()
    cur.execute("SELECT x.comment FROM comments x where id = (SELECT max(id) FROM comments)")
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result[0][0]


def generate_link_for_get_payment(comment, CONST_AMOUNT):
    ''' Генерируется ссылка на оплату с комментарием из create_comment '''
    some_comment = comment
    return pyqiwi.generate_form_link(pid=99, account='+79777288083', amount=CONST_AMOUNT, comment=some_comment, blocked=None, account_type=0)


def checking_is_payment_done(comment, CONST_AMOUNT):
    ''' Возвращает True если есть такой комментарий и оплачена верная сумма '''
    conn = sqlite3.connect('bot_DB.db')
    cur = conn.cursor()
    sql = "select 1 where exists (select x.comment from payment x, payment y where x.comment = y.comment and x.amount = (?) and x.comment = (?))"
    cur.execute(sql, (CONST_AMOUNT, comment,))
    result = cur.fetchall()
    conn.commit()
    conn.close()
    if result == []:
        return False
    elif result[0][0] == 1:
        return True
    else:
        return 'break'
