import warnings
from .SocketConnection import SocketConnection


class ChannelManager:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection_dict = {}  # (host, port) channel

    def send_message(self, message):
        message.source_dict = {"host": self.host, "port": self.port}
        # ajouter hash, signature...
        message.add_created_at()

        if message.destination_dict is not None:
            # envoie unique
            if (message.destination_dict["host"], message.destination_dict["port"]) not in self.connection_dict:
                # on a pas de channel
                channel = SocketConnection(message.destination_dict["host"], message.destination_dict["port"]).create_client()
                self.add_channel(channel=channel, **message.destination_dict)

            # envoie message
            self.connection_dict[(message.destination_dict["host"], message.destination_dict["port"])].send_message(message)

        else:
            # broadcast
            pass


    def add_channel(self, host, port, channel):
        if (host, port) in self.connection_dict:
            warnings.warn("On va écraser un channel")
        self.connection_dict[(host, port)] = channel