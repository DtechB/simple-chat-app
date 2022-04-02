import socket
import threading
import os

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

    def send_private(self, message, username):
        for connection in self.connection:
            if connection.username == username:
                connection.send(message)

    def remove_connection(self, connection):
        self.connection.remove(connection)


class ServerSocket(threading.Thread):
    def __init__(self, sc, sock_name, server):
        super().__init__()
        self.sc = sc
        self.sock_name = sock_name
        self.server = server
        self.username = None

    def run(self):
        while True:
            message = self.sc.recv(1024).decode('UTF-8')
            if message:
                print(message)
                if message.find('Make') != -1:
                    username, password = p.split_data(message)
                    self.username = username
                    msg = user.create_user(username, password)
                    self.sc.send(msg.encode())

                elif message.find('Connect') != -1:
                    username, password = p.split_data(message)
                    self.username = username
                    msg = user.login_user(username, password)
                    self.sc.send(msg.encode())

                elif message.find('Group') != -1:
                    username, room_name = p.split_data(message)
                    msg = room.add_user_to_room(username, room_name)
                    msg2 = p.s_join_welcome(username)
                    self.sc.send(msg2.encode())
                    self.server.broadcast(msg, self.sock_name)

                elif message.find('Users') != -1:
                    msg = room.get_all_user_in_room('computer')
                    self.sc.send(msg.encode())

                elif message.find('GM') != -1:
                    room_name, message_len, message_body = p.split_data(message)
                    msg = p.s_send_message_all(self.username, room_name, message_body)
                    self.server.broadcast(msg, self.sock_name)

                elif message.find('END') != -1:
                    msg = p.s_leave_user(self.username)
                    self.sc.sendall(msg.encode())

                elif message.find('QUIT') != -1:
                    pass
                else:
                    message_len, to, message_body = p.split_data(message)
                    msg = p.s_send_message_private(self.username, to, message_body)
                    self.server.send_private(msg, to)
            else:
                print(f"{self.sock_name} has closed the connection")
                self.sc.close()
                self.server.remove_connection(self)
                return

    def send(self, message):
        self.sc.sendall(message.encode())


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
