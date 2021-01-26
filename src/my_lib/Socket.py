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

    def accept(self):
        client_socket, addr = self.socket.accept()
        return client_socket
        # data = conn.recv(1024).decode()
        # print(data)

        # conn.send("ok".encode())

    def start_client_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def read_canal(self, python_socket=None):
        if python_socket:
            b_message = python_socket.recv(1024)
        else:
            b_message = self.socket.recv(1024)
        return b_message.decode()

    def send_canal(self, str_message, python_socket=None):
        binary_message = str_message.encode()
        if python_socket:
            python_socket.send(binary_message)
        else:
            self.socket.send(binary_message)





