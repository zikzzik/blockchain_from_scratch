import socket
from Socket import Socket


class Miner:

    def __init__(self, host="", port=9000, connection_host=None, connection_port=None, connection_list_size=10):
        self.host = host
        self.port = port
        self.connection_host = connection_host
        self.connection_port = connection_port
        self.connection_list_size = connection_list_size
        self.is_first = True if connection_host is None else False

        self.server_socket = Socket("server", self.host, self.port, self.connection_list_size)

        if self.is_first is False:
            self.initialization()

        self.launch_server()


    def launch_server(self):
        print("Le serveur écoute à présent sur le port {}".format(self.port))

        while True:
            client_socket, str_message = self.server_socket.read_message_with_server()

            print(str_message)

            client_socket.send(b"Liste des serveurs")




    def initialization(self):
        self.server_socket = Socket("client", self.connection_host, self.connection_port)
        self.server_socket.send_message("Salut je suis nouveau, give liste")


