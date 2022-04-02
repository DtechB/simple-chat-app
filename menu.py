from database import room


def enter_menu():
    print("----------------------------------------")
    print("|               choose one             |")
    print("|--------------------------------------|")
    print("| 1- sign up        | 2- login         |")
    print("----------------------------------------")
    option = input("choose: ")
    return option


def choose_room():
    print("----------------------------------------")
    print("|         choose room to join          |")
    print("|--------------------------------------|")
    print("| 1- computer                          |")
    print("----------------------------------------")
    option = input("choose: ")
    return option


def main_menu():
    print("----------------------------------------")
    print("|          choose one option           |")
    print("|--------------------------------------|")
    print("| 1- list of all users in this room    |")
    print("| 2- sending message generally         |")
    print("| 3- sending message private           |")
    print("| 4- leave room and exit               |")
    print("----------------------------------------")
    option = input("choose: ")
    return option
