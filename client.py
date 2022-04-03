import socket
import sys
import threading
import os
import tkinter as tk
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
                if self.message:
                    self.message.insert(tk.END, message)
                    print('\r{}\n{}: '.format(message, self.name), end='')
                else:
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
        message.get_all_messages()

        send.start()
        receive.start()

        return receive

    def send(self, textInput):
        message = textInput.get()
        textInput.delete(0, tk.END)
        self.message.insert(tk.END, '{}: {}'.format(self.username, message))
        if message == "QUIT":
            self.sock.sendall('server: {} has left the room'.format(self.username).encode())
            print("\nQuiting")
            self.sock.close()
            os._exit(0)
        else:
            self.sock.sendall('{}: {}'.format(self.username, message).encode())


def main(host, port):
    client = Client(host, port)
    receive = client.start()

    window = tk.Tk()
    window.title('chatroom')
    from_message = tk.Frame(master=window)
    scroll_bar = tk.Scrollbar(master=from_message)
    message = tk.Listbox(master=from_message, yscrollcommand=scroll_bar.set)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    message.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    client.message = message
    receive.message = message
    from_message.grid(row=0, column=0, columnspan=2, sticky="nsew")
    from_entry = tk.Frame(master=window)
    text_input = tk.Entry(master=from_entry)
    text_input.pack(fill=tk.BOTH, expand=True)
    text_input.bind("<Return>", lambda x: client.send(text_input))
    text_input.insert(0, "write your message here.")

    btn_send = tk.Button(
        master=window,
        text="Send",
        command=lambda: client.send(text_input)
    )
    from_entry.grid(row=1, column=0, padx=10, sticky="ew")
    btn_send.grid(row=1, column=1, pady=10, sticky="ew")

    window.rowconfigure(0, minsize=500, weight=1)
    window.rowconfigure(1, minsize=50, weight=0)
    window.columnconfigure(0, minsize=500, weight=1)
    window.columnconfigure(1, minsize=200, weight=0)

    window.mainloop()


if __name__ == "__main__":
    main('127.0.0.1', 50000)
