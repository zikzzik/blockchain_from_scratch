from .Socket import Socket


class Message:


    def __init__(self, message, ):
        self.message = message

    def send(self, host, port):
        socket = Socket("client", host, port)
        socket.send_canal(self.message)
        message = socket.read_canal()
        return message
