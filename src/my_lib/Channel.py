from .Message import Message
from socket import socket


class Channel:
    def __init__(self, my_socket: socket, host: str, port: int):
        self.my_socket = my_socket
        self.host = host
        self.port = port

    def send_message(self, message: Message):
        binaries = message.to_binary()
        self.my_socket.send(binaries)

    def read_message(self) -> Message:
        # the best way is to send a first message with the size before
        bin_message = self.my_socket.recv(1000000000)  # 1Go
        return Message.from_binary(bin_message)