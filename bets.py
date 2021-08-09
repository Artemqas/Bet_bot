import sqlite3

def insert_into_bets(sport, text):
        conn = sqlite3.connect('bot_DB.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO bets(sport_name, text_bet) VALUES (?, ?)", (sport, text))
        conn.commit()
        conn.close()

def get_last_bet(sport):
    conn = sqlite3.connect('bot_DB.db')
    cur = conn.cursor()
    cur.execute("SELECT text_bet FROM bets WHERE id = (SELECT max(id) FROM (SELECT * FROM bets WHERE sport_name = (?)))", (sport,))
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result[0][0]
