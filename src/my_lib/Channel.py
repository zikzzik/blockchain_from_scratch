from .Message import Message


class Channel:
    def __init__(self, my_socket, host, port):
        self.my_socket = my_socket
        self.host = host
        self.port = port

    def send_message(self, message: Message):
        binaries = message.to_binary()
        self.my_socket.send(binaries)

    def read_message(self) -> Message:
        bin_message = self.my_socket.recv(1024)
        return Message.from_binary(bin_message)