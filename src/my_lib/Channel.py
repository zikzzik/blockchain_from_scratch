import socket


class Channel:
    def __init__(self, my_socket, host, port):
        self.my_socket = my_socket
        self.host = host
        self.port = port

    def send_message(self, str_message):
        binary_message = str_message.encode()
        self.my_socket.send(binary_message)

    def read_message(self):
        b_message = self.my_socket.recv(1024)
        return b_message.decode()