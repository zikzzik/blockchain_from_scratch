import random
from datetime import datetime
from .SocketConnection import SocketConnection
from .Message import Message
from .ChannelManager import ChannelManager
from .Block import Block
from .Blockchain import Blockchain
from .Transaction import Transaction
import time
import threading


class Miner:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 9000,
        connection_host: str = None,
        connection_port: int = None,
        difficulty: int = 3,
    ):
        self.host = host
        self.port = port
        self.difficulty = difficulty
        self.lock = threading.Lock()
        self.blockchain = Blockchain(self.lock)
        self.waiting_transaction = set()

        self.channel_manager = ChannelManager(host, port)

        self.is_first = False if all([connection_host, connection_port]) else True
        if self.is_first is False:
            self.join_pool({"host": connection_host, "port": connection_port})
        self.socket_connection = SocketConnection(self.host, self.port).create_server()
        threading.Thread(target=self.start_mine).start()
        self.launch_server()

    def launch_server(self):
        print("Le serveur écoute à présent sur le port {}".format(self.port), flush=True)

        while True:
            channel, _ = self.socket_connection.accept()
            message = channel.read_message()
            origin_host, origin_port = message.get_source()
            self.channel_manager.add_server(origin_host, origin_port)
            threading.Thread(target=self.route_message, args=(channel, message)).start()

    def join_pool(self, destination: dict):
        message_in = Message("join_pool", destination=destination)
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
        threading.Thread(target=self.mine_block_thread, args=(block, heart_bit_interval, (0, 2))).start()
        threading.Thread(target=self.mine_block_thread, args=(block, heart_bit_interval, (1, 2))).start()

    def mine_block_thread(self, block: Block, heart_bit_interval=0.1, strat=(0, 1)):
        """
            CARE DELETE THREAD ID
        Args:
            block:
            heart_bit_interval:
            strat: (start, increment) (0, 2) -> tous les nonces % 2 == 0 seront traités

        Returns:

        """
        nonce = strat[0]
        last_heart_bit = time.time()
        while True:
            block.set_nonce(nonce)

            if block.is_correct(difficulty=self.difficulty):
                print(block.nonce)
                if self.blockchain.get_idx_last_block() < block.get_index():
                    self.blockchain.add_block(block)
                    return None
                else:
                    return None
            # @ todo tmp comment for hash calcul
            # if last_heart_bit + heart_bit_interval > time.time():
            #     if self.blockchain.get_idx_last_block() >= block.get_index():
            #         return None
            nonce += strat[1]

    def start_mine(self):
        # TODO Code pas beau / devra être lancé dans un thread
        # b = Block(index=1, previous_hash="None", block_size=10, nonce=0, timestamp=None)

        ts = int(datetime.timestamp(datetime(2000, 6, 1, 12, 12)))
        b = Block(index=2, previous_hash="000a18ee3d4a4229016502b4bb6702b3147095000cd2595f980458cd0bae76fd", block_size=3, timestamp=ts)
        b.add_transaction(Transaction("zak", "sylvain", 10000, ts))
        b.add_transaction(Transaction("antoine", "zak", 5000, ts))
        b.add_transaction(Transaction("zak", "antoine", 30, ts))

        self.mine_block(b)
        print(self.blockchain)

    def broadcast_blockchain(self):
        # @todo des que j'update ma blockchain, je broadcast
        pass

    def broadcast_transaction(self):
        # @todo si je recois une nouvelle transaction qui n'est pas dans la blockchain et pas dans ma liste: je broadcast
        pass

    def update_blockchain(self):
        # @todo  Faire des controlles sur cette blockchain (taille et validité)
        # si je recois une meilleure blockchain alors j'écrase la mienne
        pass
