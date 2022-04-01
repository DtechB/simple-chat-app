import sqlite3
from database.commands import GET_USER_BY_USERNAME


def register_user_validation(username, password):
    with sqlite3.connect('db.sqlite3') as conn:
        cur = conn.cursor()
        cur.execute(GET_USER_BY_USERNAME, (username,))
        data = cur.fetchall()
        if len(data) != 0:
            return f"user already registered"
        if len(password) < 6:
            return f"password must be at least 6 character"
        return 'success'


def login_user_validation(username, password):
    with sqlite3.connect('db.sqlite3') as conn:
        cur = conn.cursor()
        cur.execute(GET_USER_BY_USERNAME, (username,))
        user = cur.fetchall()
        if len(user) == 0:
            return f"this username is not exist"
        user = user[0]
        if user[2] != password:
            return f"username and password are not same"
        return 'success'
