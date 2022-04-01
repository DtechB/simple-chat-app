import socket
import sys
import threading
import os
import tkinter as tk
from database import user
import protocol as p


class Send(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        while True:
            print('{} '.format(self.name), end='')
            sys.stdout.flush()
            message = input()
            if message == 'QUIT':
                self.sock.sendall('Server: {} has left the chat.'.format(self.name).encode())
                break

            else:
                self.sock.sendall('{}: {} '.format(self.name, message).encode())
        print("\nQuiting")
        self.sock.close()
        os.exit(0)


class Receive(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.message = None

    def run(self):
        message = self.sock.recv(1024).decode('UTF-8')

        if message:
            if self.message:
                self.message.insert(tk.END, message)
                print('hi')
                print('\r{}\n{}: '.format(message, self.name), end='')
            else:
                print('\r{}\n{}: '.format(message, self.name), end='')
        else:
            print("\nlost connection")
            self.sock.close()
            os.exit(0)


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.password = None
        self.message = None

    def sign_up(self):
        self.username = input("Enter a unique username: ")
        self.password = input("Enter your password: ")
        return p.c_register(self.username, self.password)

    def start(self):
        self.sock.connect((self.host, self.port))
        print("successfully connected to {}:{}".format(self.host, self.port))
        msg = self.sign_up()
        self.sock.send(msg.encode())
        print('welcome get ready for sending and receiving message')

        send = Send(self.sock, self.username)
        receive = Receive(self.sock, self.username)

        send.start()
        receive.start()

        self.sock.sendall('server: {} joined the chat'.format(self.username).encode())
        print('\rReady! typing QUIT for exit.\n')
        print('{}: '.format(self.username), end='')
        return receive

    def send(self, textInput):
        message = textInput.get()
        textInput.delete(0, tk.END)
        self.message.insert(tk.END, )


if __name__ == "__main__":
    client = Client('127.0.0.1', 50000)
    receive = client.start()
