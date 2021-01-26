import socket
import sys


class Sender:

    def __init__(self, first_connection_host=None, first_connection_port=None):
        self.connection_dict = {}
        self.first_connection_host = first_connection_host
        self.first_connection_port = first_connection_port

        if all((self.first_connection_host, self.first_connection_port)):
            self.first_connection()


    def send_message(self, host, port, str_message):
        assert (host, port) in self.connection_dict, "recipient not found"

        recipient_socket = self.connection_dict[(host, port)]
        binary_message = str_message.encode()
        recipient_socket.send(binary_message)
        message = recipient_socket.recv(1024)
        print(message)
        return True

    def add_connection(self, host, port, my_socket):
        self.connection_dict[(host, port)] = my_socket

    def first_connection(self):
        my_socket = self.create_socket(self.first_connection_host, self.first_connection_port)
        self.add_connection(self.first_connection_host, self.first_connection_port, my_socket)
        self.send_message(self.first_connection_host, self.first_connection_port, "Coucou je vous rejoins")

    def create_socket(self, host, port):
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.connect((host, port))
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return my_socket

    def read_canal(self, client_socket):
        b_message = client_socket.recv(1024)
        return b_message.decode()