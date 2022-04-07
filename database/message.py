import database.commands as c
import protocol as p
from database import user


def save_message(message, username):
    user_id = user.get_user_id(username)
    c.insert(c.CREATE_MESSAGE, (message, user_id))


def get_all_messages(username):
    data = c.select(c.GET_ALL_MESSAGES, ())
    for message in data:
        if message[1].find('PM') != -1:
            users = p.split_data(message[1])
            from_user = users[0]
            to_user = users[1]
            if username == from_user or username == to_user:
                print(f"{message[4]}: {message[1]}")
        else:
            print(f"{message[4]}: {message[1]}")
