import socket
from .Socket import Socket
from .Sender import Sender
from .Receiver import Receiver
import time


# class Miner:
#
#     def __init__(self, host="localhost", port=9000, connection_host=None, connection_port=None, connection_list_size=10):
#         self.host = host
#         self.port = port
#         self.connection_host = connection_host
#         self.connection_port = connection_port
#         self.connection_list_size = connection_list_size
#         self.is_first = True if any([connection_host, connection_port]) else False
#
#
#
#
#         # if self.is_first is False:
#             # self.initialization()
#         # else:
#         self.launch_server()
#
#
#     # async
#     def launch_server(self):
#
#         self.server_socket = Socket("server", self.host, self.port, self.connection_list_size)
#
#         print("Le serveur écoute à présent sur le port {}".format(self.port), flush=True)
#         while True:
#             client_socket = self.server_socket.accept()
#             message = self.server_socket.read_canal(client_socket)
#             print(message)
#             self.server_socket.send_canal(f"Bien recu", client_socket)
#             # client_socket.send(b"Liste des serveurs")





class Miner:

    def __init__(self, host="localhost", port=9000, connection_host=None, connection_port=None,
                 connection_list_size=10):
        self.host = host
        self.port = port
        self.connection_host = connection_host
        self.connection_port = connection_port
        self.connection_list_size = connection_list_size
        self.is_first = True if any([connection_host, connection_port]) else False

        self.sender = Sender(self.connection_host, self.connection_port)
        self.receiver = Receiver(self.host, self.port, self.connection_list_size)

        self.launch_server()

    # async
    def launch_server(self):
        print("Le serveur écoute à présent sur le port {}".format(self.port), flush=True)

        while True:
            client_socket, (host, port) = self.receiver.accept()
            self.sender.add_connection(host, port, client_socket)
            message = self.receiver.read_canal(client_socket)
            self.route_message(message)
            client_socket.send(b"bien recu first")
            self.sender.send_message(host, port, "Bien recu second")



    def route_message(self, message):
        print(f"Fais action calcule avec parametre {message}")


