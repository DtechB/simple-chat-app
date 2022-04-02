import socket
import threading
import os
import time

from database import user, room
import protocol as p

lock = threading.Lock()


class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.connection = []
        self.host = host
        self.port = port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))

        sock.listen(1)
        print("listening at ", sock.getsockname())

        while True:
            sc, sock_name = sock.accept()
            print(f"accepting a new connection from {sock_name}")

            server_socket = ServerSocket(sc, sock_name, self)
            server_socket.start()

            self.connection.append(server_socket)
            print("ready to receive message from ", sc.getpeername())

    def broadcast(self, message, source):
        for connection in self.connection:
            if connection.sock_name != source:
                connection.send(message)

    def remove_connection(self, connection):
        self.connection.remove(connection)


class ServerSocket(threading.Thread):
    def __init__(self, sc, sock_name, server):
        super().__init__()
        self.sc = sc
        self.sock_name = sock_name
        self.server = server

    def run(self):
        while True:
            message = self.sc.recv(1024).decode('ascii')
            if message:
                print(message)
                if message.find('Make') != -1:
                    print(message)
                    username, password = p.split_data(message)
                    msg = user.create_user(username, password)
                    self.sc.send(msg.encode('ascii'))

                elif message.find('Connect') != -1:
                    print(message)
                    username, password = p.split_data(message)
                    msg = user.login_user(username, password)
                    self.sc.send(msg.encode('ascii'))

                elif message.find('Group') != -1:
                    print(message)
                    username, room_name = p.split_data(message)
                    msg = room.add_user_to_room(username, room_name)
                    msg2 = p.s_join_welcome(username)
                    self.sc.send(msg2.encode('ascii'))
                    self.server.broadcast(msg, self.sock_name)

                elif message.find('Users') != -1:
                    print(message)
                    msg = room.get_all_user_in_room('computer')
                    self.sc.send(msg.encode('ascii'))
                else:
                    self.server.broadcast(message, self.sock_name)
            else:
                print(f"{self.sock_name} has closed the connection")
                self.sc.close()
                self.server.remove_connection(self)
                return

    def send(self, message):
        self.sc.sendall(message.encode('ascii'))


def _exit_(server):
    while True:
        ipt = input()
        if ipt == 'q':
            print("closing all connection...")
            for connection in server.connection:
                connection.sc.close()
            os._exit(0)


if __name__ == '__main__':
    server = Server('127.0.0.1', 50000)
    server.start()
    finish = threading.Thread(target=_exit_, args=(server,))
    finish.start()
