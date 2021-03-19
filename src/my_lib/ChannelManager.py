import warnings
from .SocketConnection import SocketConnection
from .Channel import Channel


class ChannelManager:

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.connections: set = {(host, port)}  # (host, port) channel

    def send_message(self, message) -> [Channel, None]:
        message.set_source(self.host, self.port)
        message.add_created_at()

        if message.destination is not None and message.broadcast is False:
            # simple send
            assert len(message.destination) == 2, "No destination in message"
            channel = SocketConnection(message.destination["host"], message.destination["port"]).create_client()
            if channel is not False:
                channel.send_message(message)
            else:
                print(f"can't send message to {message.destination['host']}:{message.destination['port']}")
            return channel
        elif message.destination is None and message.broadcast is True:
            # broadcast
            for host, port in self.connections:
                if (host, port) == (self.host, self.port):
                    continue
                channel = SocketConnection(host, port).create_client()
                if channel is not False:
                    channel.send_message(message)
                else:
                    print(f"can't send message to {host}:{port}")
            return None
        else:
            raise ValueError("Message have broadcast True and destination")

    def add_server(self, host, port):
        self.connections.add((host, port))

    def get_connections(self):
        return self.connections

    def answer_message(self, channel, message):
        channel.send_message(message)