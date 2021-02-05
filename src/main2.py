from my_lib import Miner, Message, ChannelManager


if __name__ == "__main__": 

    c = ChannelManager("localhost", 9000)

    c.send_message(Message("start_mine", destination={"host": "localhost", "port": 8000}))
