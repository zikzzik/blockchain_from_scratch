import socket
from .Socket import Socket
import time


class Miner:

    def __init__(self, host="localhost", port=9000, connection_host=None, connection_port=None, connection_list_size=10):
        self.host = host
        self.port = port
        self.connection_host = connection_host
        self.connection_port = connection_port
        self.connection_list_size = connection_list_size
        self.is_first = True if connection_host is None else False

        self.server_socket = Socket("server", self.host, self.port, self.connection_list_size)


        # if self.is_first is False:
            # self.initialization()
        # else:
        self.launch_server()


    def launch_server(self):

        print("Le serveur écoute à présent sur le port {}".format(self.port), flush=True)
        i = 0
        while True:
            self.server_socket.start_server_socket()
            client_socket = self.server_socket.accept()
            message = self.server_socket.read_canal(client_socket)
            print(message)
            self.server_socket.send_canal(f"Bien recu {i}", client_socket)
            # client_socket.send(b"Liste des serveurs")
            i += 1



    # def initialization(self):
    #     self.server_socket = Socket("client", self.connection_host, self.connection_port)
    #     self.server_socket.send_message("Salut je suis nouveau, give liste")
    #     time.sleep(2)


