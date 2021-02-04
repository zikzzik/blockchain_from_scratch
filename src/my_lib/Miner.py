import random

from .SocketConnection import SocketConnection
from .Message import Message
from .ChannelManager import ChannelManager
from .Block import Block
from .Blockchain import Blockchain
import time
import threading


class Miner:

    def __init__(self, host="localhost", port=9000, connection_host=None, connection_port=None, difficulty=1):
        self.host = host
        self.port = port
        self.difficulty = difficulty
        self.blockchain = Blockchain()

        self.channel_manager = ChannelManager(host, port)

        self.is_first = False if all([connection_host, connection_port]) else True
        if self.is_first is False:
            self.join_pool({"host": connection_host, "port": connection_port})
        self.socket_connection = SocketConnection(self.host, self.port).create_server()
        # self.launch_server()


    def launch_server(self):
        print("Le serveur écoute à présent sur le port {}".format(self.port), flush=True)

        while True:
            channel, (host, port) = self.socket_connection.accept()
            self.channel_manager.add_server(host, port)
            message = channel.read_message()
            self.route_message(channel, message)

            # channel.send_message(Message("ok"))

    def join_pool(self, destination: dict):
        message_in = Message("join_pool", destination=destination)
        # channel.send_message(message_in)
        channel = self.channel_manager.send_message(message_in)
        m = channel.read_message()
        print(f"Pool join  -> {m}")

    def new_server_accepted(self, channel, message):
        print(f"New server accepted : {message.source}")
        message = Message("connection_list", content=self.channel_manager.get_connections())
        self.channel_manager.answer_message(channel, message)

    def route_message(self, channel, message: Message):
        action_dict = {"join_pool": self.new_server_accepted}
        action_dict[message.m_type](channel, message)


    def mine_block(self, block: Block, heart_bit_interval=0.1):
        thread_id_1 = random.randrange(0, 999999)
        thread_id_2 = random.randrange(0, 999999)
        threading.Thread(target=self.mine_block_thread, args=(block, heart_bit_interval, thread_id_1, (0, 2))).start()
        threading.Thread(target=self.mine_block_thread, args=(block, heart_bit_interval, thread_id_2, (1,2))).start()


    def mine_block_thread(self, block: Block, heart_bit_interval=0.1, thread_id=-1, strat=(0, 1)):
        """

        :param block:
        :param heart_bit_interval:
        :param thread_id:
        :param strat: (start, increment) (2, 0) -> tous les nonces % 2 == 0 seront traité
        :return:
        """
        nonce = strat[0]
        last_heart_bit = time.time()
        while True:
            block.set_nonce(nonce)

            if block.is_correct(difficulty=self.difficulty):
                if self.blockchain.get_idx_last_block() < block.get_index():
                    self.blockchain.add_block(block)
                    print("succes")
                    return None
                else:
                    return None

            if last_heart_bit + heart_bit_interval > time.time():
                if not self.blockchain.get_idx_last_block() < block.get_index():
                    return None
            nonce += strat[1]

            # print(f"id : {thread_id} -> {nonce}")

