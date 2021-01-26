from .SocketConnection import SocketConnection


class Miner:

    def __init__(self, host="localhost", port=9000, connection_host=None, connection_port=None):
        self.host = host
        self.port = port

        self.is_first = True if any([connection_host, connection_port]) else False

        if self.is_first is False:
            self.join_pool(connection_host, connection_port)
        self.socket_connection = SocketConnection(self.host, self.port).create_server()
        self.launch_server()

    # async
    def launch_server(self):
        print("Le serveur écoute à présent sur le port {}".format(self.port), flush=True)

        while True:
            channel = self.socket_connection.accept()
            message = channel.read_message()
            self.route_message(message)
            channel.send_message("bien recu first")


    def join_pool(self, host, port):
        join_socket = SocketConnection(host, port).create_client(host, port)



    def route_message(self, message):
        print(f"Fais action calcule avec parametre {message}")


