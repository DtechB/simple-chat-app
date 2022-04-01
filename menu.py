

def enter_menu(register, login):
    print("----------------------------------------")
    print("|               choose one             |")
    print("|--------------------------------------|")
    print("| 1- sign up        | 2- login         |")
    print("----------------------------------------")
    option = input("choose: ")
    switcher = {
        1: register()
    }

