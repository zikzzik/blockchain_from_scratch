import socket


class Socket:

    def __init__(self, socket_type, host, port, connection_list_size=10):
        self.socket_type = socket_type
        self.host = host
        self.port = port
        self.connection_list_size = connection_list_size

        self.socket = None
        if self.socket_type == "client":
            self.start_client_socket()
        elif self.socket_type == "server":
            self.start_server_socket()
        else:
            raise NotImplementedError(f"Socket type only client or server (not {self.socket_type}")

    def start_server_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.connection_list_size)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start_client_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send_message(self, str_message):
        assert self.socket_type == "client", "Only client can send message"

        binary_message = str_message.encode()
        self.socket.send(binary_message)

    async def start_listen(self):
        pass