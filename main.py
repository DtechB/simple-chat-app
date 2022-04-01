import protocol as p
from database import commands as c
from database.room import get_all_user_in_room
import sqlite3


if __name__ == "__main__":
    print(get_all_user_in_room('computer'))
