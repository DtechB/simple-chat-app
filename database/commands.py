import sqlite3

CREATE_USER = 'INSERT INTO Users(username, password) VALUES(?, ?)'
ALL_USERS = 'SELECT * FROM Users'
GET_USER_BY_USERNAME = 'SELECT * FROM Users WHERE username=?'
GET_USER_BY_ID = 'SELECT * FROM Users WHERE id=?'
GET_ROOM_BY_NAME = 'SELECT * FROM Room WHERE name=?'
ALL_USERS_IN_ROOM = 'SELECT * FROM main.Users INNER JOIN ' \
                    'main.Room ON Users.room = Room.id WHERE room.id=?'


def insert(command, data):
    with sqlite3.connect('db.sqlite3') as conn:
        conn.execute(command, data)
        conn.commit()


def select(command, data):
    with sqlite3.connect('db.sqlite3') as conn:
        cur = conn.cursor()
        cur.execute(command, data)
        return cur.fetchall()
