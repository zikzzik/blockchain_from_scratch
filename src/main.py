from my_lib.Miner import Miner
from my_lib.Socket import Socket


if __name__ == "__main__":
    Miner()

    # import socket
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.bind(("localhost", 9000))
    # sock.listen(2)
    # conn, addr = sock.accept()
    # data = conn.recv(1024).decode()
    # print(data)
    # Socket("server", "localhost", 9000)