import database.commands as c
import protocol as p


def get_room_by_id(room):
    data = c.select(c.GET_ROOM_BY_NAME, (room, ))
    return data[0][0]


def get_all_user_in_room(room):
    room_id = get_room_by_id(room)
    data = c.select(c.ALL_USERS_IN_ROOM, (room_id,))
    users_list = [item[1] for item in data]
    return p.s_show_online_users(users_list)


def add_user_to_room(username, room):
    room_id = get_room_by_id(room)
    c.update(c.ADD_USER_TO_ROOM, (room_id, username))
    return p.s_join_inform_all_users(username)
