from .SocketConnection import SocketConnection
from .Message import Message


class Miner:

    def __init__(self, host="localhost", port=9000, connection_host=None, connection_port=None):
        self.host = host
        self.port = port

        self.is_first = False if all([connection_host, connection_port]) else True
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
            channel.send_message(Message("ok"))

    def join_pool(self, host, port):
        # @todo  ajouter ce channel au reférentiel
        channel = SocketConnection(host, port).create_client(host, port)
        message_in = Message("join_pool")
        channel.send_message(message_in)
        message_out = channel.read_message()
        print(f"Reply: pool join ? -> {message_out}")

    def new_server_accepted(self, message):
        print("New server accepted : <ADD IP:PORT>")

    def route_message(self, message: Message):
        action_dict = {"join_pool": self.new_server_accepted}
        action_dict[message.m_type](message)
        


