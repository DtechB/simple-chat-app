import sqlite3
from database.commands import CREATE_USER, GET_USER_BY_USERNAME
import validation as v
import protocol as p


def get_user_id(username):
    with sqlite3.connect('db.sqlite3') as conn:
        cur = conn.cursor()
        cur.execute(GET_USER_BY_USERNAME, (username,))
        user = cur.fetchall()
        return user[0][0]


def create_user(username, password):
    message = v.register_user_validation(username, password)
    if message == "success":
        with sqlite3.connect('db.sqlite3') as conn:
            conn.execute(CREATE_USER, tuple((username, password)))
            conn.commit()
        user_id = get_user_id(username)
        return p.s_register_accepted(user_id)

    return p.s_register_rejected(message)


def login_user(username, password):
    message = v.login_user_validation(username, password)
    if message == 'success':
        user_id = get_user_id(username)
        return p.s_login_connected(user_id)

    return p.s_login_error(message)


