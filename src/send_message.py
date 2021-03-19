from my_lib import Miner, Message, ChannelManager, Transaction, Blockchain
import time

ts = int(time.time())

if __name__ == "__main__":

    c = ChannelManager("localhost", 10000)
    message = Message("TRANSACTION", Transaction("a", "b", 12, ts), destination={"host": "localhost", "port": 8000})
    c.send_message(message)
