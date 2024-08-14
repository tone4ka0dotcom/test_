import sqlite3


def create_db():
    connection = sqlite3.connect('game_database.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
    username TEXT,
    points INTEGER
    )
    ''')
    connection.commit()
    connection.close()


def add_el(name, point):
    connection = sqlite3.connect('game_database.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO players (username, points) VALUES (?, ?)", (name, point))
    connection.commit()
    connection.close()


def update_db(name, point):
    connection = sqlite3.connect('game_database.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE players SET points = ? WHERE username = ?', (point, name))
    connection.commit()
    connection.close()


create_db()
