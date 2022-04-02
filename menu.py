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
    print("-------------------------------------------------------------------")
    print("|                             Help                                |")
    print("|-----------------------------------------------------------------|")
    print("| 1- list of all users in this room by typing USERS               |")
    print("| 2- sending message generally by typing GM first of message      |")
    print("| 3- sending message private by typing username first of message  |")
    print("| 4- leave room by typing QUIT                                    |")
    print("| 5- show help by typing HELP                                     |")
    print("-------------------------------------------------------------------")
    input("press any key to continue: ")
