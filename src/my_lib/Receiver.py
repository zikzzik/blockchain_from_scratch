import socket


class Receiver:

    def __init__(self, host, port, connection_list_size):
        self.host = host
        self.port = port
        self.connection_list_size = connection_list_size

        self.create_socket()

    def create_socket(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.bind((self.host, self.port))
        self.my_socket.listen(self.connection_list_size)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def accept(self):
        client_socket, addr = self.my_socket.accept()
        print("DEBUG addr : ", addr, type(addr))
        return client_socket

    def read_canal(self, client_socket):
        b_message = client_socket.recv(1024)
        return b_message.decode()