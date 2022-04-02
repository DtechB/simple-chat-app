import database.commands as c
from database import user


def save_message(message, username):
    user_id = user.get_user_id(username)
    c.insert(c.CREATE_MESSAGE, (message, user_id))


def get_all_messages():
    data = c.select(c.GET_ALL_MESSAGES, ())
    for message in data:
        print(f"{message[4]}: {message[1]}")
