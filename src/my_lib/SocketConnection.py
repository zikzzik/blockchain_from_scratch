import socket
from .Channel import Channel


class SocketConnection:

    def __init__(self, host, port, connection_list_size=10):
        self.host = host
        self.port = port
        self.connection_list_size = connection_list_size
        self.my_socket = None


    def create_server(self):
        assert self.my_socket is None, "Socket already used"
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.bind((self.host, self.port))
        self.my_socket.listen(self.connection_list_size)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return self

    def accept(self):
        client_socket, (host, port) = self.my_socket.accept()
        return Channel(client_socket, host, port), (host, port)

    def create_client(self):
        assert self.my_socket is None, "Socket already used"
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.connect((self.host, self.port))
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return Channel(self.my_socket, self.host, self.port)


    "{(host, port): socket}"

