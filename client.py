import socket
import sys
import threading
import os
import menu
import protocol as p
from database import message, room


class Send(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        while True:
            print('{}: '.format(self.name), end='')
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]
            if message == 'QUIT':
                msg = p.c_leave(self.name)
                self.sock.send(msg.encode())
                room.remove_user_from_room(self.name)
                break
            elif message == 'USERS':
                msg = p.c_get_online_users(self.name)
                self.sock.send(msg.encode())
            elif message.find('GM') != -1:
                message = message[3:]
                msg = p.c_send_message_all('computer', message)
                self.sock.send(msg.encode())
            elif message == 'HELP':
                menu.main_menu()
            else:
                data = message.split(' ')
                user = data[0]
                message = ''
                for word in data:
                    if word != user:
                        message += word + ' '
                msg = p.c_send_message_private(user, message)
                self.sock.send(msg.encode())
        print("\nQuiting")
        self.sock.close()
        os._exit(0)


class Receive(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.message = None

    def run(self):
        while True:
            message = self.sock.recv(1024).decode('UTF-8')
            if message:
                print('\r{}\n{}: '.format(message, self.name), end='')
            else:
                print("\nlost connection")
                self.sock.close()
                os._exit(0)


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.password = None
        self.message = None
        self.roomName = None

    def sign_up(self):
        self.username = input("Enter a unique username: ")
        self.password = input("Enter your password: ")
        return p.c_register(self.username, self.password)

    def login(self):
        self.username = input("Enter your username: ")
        self.password = input("Enter your password: ")
        return p.c_login(self.username, self.password)

    def start(self):
        self.sock.connect((self.host, self.port))
        print("successfully connected to {}:{}".format(self.host, self.port))
        print(self.sock.getsockname(), ' ', self.sock.getpeername())

        # show menu for login or register by user
        while True:
            option = menu.enter_menu()
            if option == '1':
                msg = self.sign_up()
            else:
                msg = self.login()
            self.sock.send(msg.encode())
            msg = self.sock.recv(1024).decode('UTF-8')
            print(msg)
            if msg.find('reason') == -1:
                break
        menu.choose_room()
        msg = p.c_join_room(self.username, 'computer')
        self.sock.send(msg.encode())
        msg = self.sock.recv(1024).decode('UTF-8')
        print(msg)

        send = Send(self.sock, self.username)
        receive = Receive(self.sock, self.username)

        menu.main_menu()
        message.get_all_messages(self.username)

        send.start()
        receive.start()

        return receive


def main(host, port):
    client = Client(host, port)
    receive = client.start()


if __name__ == "__main__":
    main('127.0.0.1', 50000)
