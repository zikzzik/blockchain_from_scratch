import socket


class Miner:

    def __init__(self, host="", port=9000, connection_ip=None, connection_port=None, connection_list_size=10):
        self.host = host
        self.port = port
        self.connection_ip = connection_ip
        self.connection_port = connection_port
        self.connection_list_size = connection_list_size
        self.is_first = True if connection_ip is None else False

        self.start_server_socket()
        self.launch_server()

    def start_server_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.connection_list_size)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print("socket créée et à l'écoute")

    def start_client_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.bind((self.host, self.port))


    def launch_server(self):
        print("Le serveur écoute à présent sur le port {}".format(self.port))

        while True:
            client_socket, connection_info = self.server_socket.accept()
            receive_message = self.server_socket.recv(1024)

            print(receive_message.decode())

            client_socket.send(b"Liste des serveurs")

            # envoyer en Thread

    def clean_socket(self):
        self.server_socket.close()

    def initialization(self):
        connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion_avec_serveur.connect((hote, port))

    def __del__(self):
        self.clean_socket()