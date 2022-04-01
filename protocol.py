# c for client
# s for server
# e for extracting data from message


def c_register(username, password):
    return f"Make -Option <user:{username}> -Option <password:{password}>"


def e_c_register(msg):
    username, password = split_data(msg)
    return {'username': username, 'password': password}


def s_register_accepted(Id):
    return f"User Accepted -Option <id:{Id}>"


def s_register_rejected(reason):
    return f"User Not Accepted -Option <reason:{reason}>"


def c_login(username, password):
    return f"Connect -Option <user:{username}> -Option <pass:{password}>"


def e_c_login(msg):
    username, password = split_data(msg)
    return {'username': username, 'password': password}


def s_login_connected(Id):
    return f"Connected -Option <id:{Id}>"


def s_login_error(reason):
    return f"ERROR -Option <reason:{reason}>"


def c_join_room(username, roomName):
    return f"Group -Option <user:{username}> -Option <gname:{roomName}>"


def e_c_join_room(msg):
    return split_data(msg)


def s_join_inform_all_users(username):
    return f"<{username}> join the chat room."


def s_join_welcome(username):
    return f"Hi <{username}>, welcome to the chat room."


def c_get_online_users(username):
    return f"Users -Option <user:{username}>"


def e_c_get_online_users(msg):
    return split_data(msg)


def s_show_online_users(data):
    users = ""
    for user in data:
        users += str(user) + "|"
    users = users[0:len(users) - 1]
    return f"USERS_LIST:\r\n{users}\r\n"


def c_send_message_all(room, msg):
    return f"GM -Option <to:{room}> -Option <message_len:{len(msg)}> " \
           f"-Option <message_body:{msg}>"


def e_c_send_message_all(room, msg):
    room, message_len, message_body = split_data(msg)
    return {'room': room, 'message': message_body, 'length': message_len}


def s_send_message_all(fromUser, room, msg):
    return f"GM -Option <from:{fromUser}> -Option <to:{room}> " \
           f"-Option <message_len:{len(msg)}> -Option <message_body:{msg}>"


def c_send_message_private(toUser, msg):
    return f"PM -Option <message_len:{len(msg)}> " \
           f"-Option <to:{toUser}> -Option <message_body:{msg}>"


def s_send_message_private(fromUser, toUser, msg):
    return f"PM -Option <from:{fromUser}> -Option <to:{toUser}> " \
           f"-Option <message_len:{len(msg)}> -Option <message_body:{msg}>"


def c_leave(name):
    return f"End -Option <id:{name}>"


def s_leave_user(username):
    return f"<{username}> left the chat room."


def split_data(msg=''):
    data = msg.split("-Option")
    data.pop(0)
    new_data = []
    for item in data:
        item = item.strip(' ')
        item = item.replace('<', '')
        item = item.replace('>', '')
        index = item.find(':')
        item = item[index+1:]
        new_data.append(item)
    return new_data
