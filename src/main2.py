from my_lib.Miner import Miner
from my_lib.Socket import Socket
from my_lib.Message import Message
from my_lib.Sender import Sender

if __name__ == "__main__": 
    # Miner(host="localhost", port=9001, connection_host="localhost", connection_port=9000)

    # import socket
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect(("localhost", 9000))
    # sock.send("hi".encode())
    # sock.send("hiiiiiii".encode())
    # sock.send(("#" * 1020).encode())

    # s = Socket("client", "localhost", 9000)
    # s.send_message("hi")
    # s.send_message("hiiiiiii")
    # print(s.socket.recv(1024))

    # m = Message("Bienvenue")
    # print(m.send("localhost", 9000))

    s = Sender("localhost", 9000)
