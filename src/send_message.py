from my_lib import Miner, Message, ChannelManager, Transaction, Blockchain
import time


if __name__ == "__main__":

    # RENANME TRANSACTION
    c = ChannelManager("localhost", 10000)
    ts = int(time.time())
    message = Message("TRANSACTION", Transaction("zak", "antoine", 12, ts),
                      destination={"host": "localhost", "port": 8000})
    c.send_message(message)

