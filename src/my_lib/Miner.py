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
import sys


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
            self.channel_manager.add_server(connection_host, connection_port)
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
        """Method use to connect to a pool miner

        Args:
            destination:

        Returns:

        """
        message_in = Message("JOIN_POOL", destination=destination)
        channel = self.channel_manager.send_message(message_in)
        if channel is False:
            sys.exit("Can't join pool, connection impossible")
        else:
            m_connection_list = channel.read_message()
            assert m_connection_list.m_type == "CONNECTION_LIST", "JOIN_POOL response message is not type 'CONNECTION_LIST'"
            print(f"Pool join")
            [self.channel_manager.add_server(host, port) for host, port in m_connection_list.content]
            self.broadcast_hi()


    def new_server_accepted(self, channel, message):
        """Method use when the miner receiver a message 'JOIN_POOL'

        Args:
            channel:
            message:

        Returns:

        """
        print(f"New server accepted : {message.source}")
        message = Message("CONNECTION_LIST", content=self.channel_manager.get_connections())
        self.channel_manager.answer_message(channel, message)

    def route_message(self, channel, message: Message):
        action_dict = {
            "JOIN_POOL": self.new_server_accepted,
            "TRANSACTION": self.receive_transaction,
            "BLOCKCHAIN": self.receive_blockchain,
            "HI": self.receive_hi,
        }
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
            if last_heart_bit + heart_bit_interval > time.time():
                if self.blockchain.get_idx_last_block() >= block.get_index():
                    return None
            nonce += strat[1]

    def start_mine(self):
        # TODO Code pas beau / devra être lancé dans un thread
        # b = Block(index=1, previous_hash="None", block_size=10, nonce=0, timestamp=None)

        # ts = int(datetime.timestamp(datetime(2000, 6, 1, 12, 12)))
        # b = Block(
        #     index=2,
        #     previous_hash="000a18ee3d4a4229016502b4bb6702b3147095000cd2595f980458cd0bae76fd",
        #     block_size=3,
        #     timestamp=ts,
        # )
        # b.add_transaction(Transaction("zak", "sylvain", 10000, ts))
        # b.add_transaction(Transaction("antoine", "zak", 5000, ts))
        # b.add_transaction(Transaction("zak", "antoine", 30, ts))
        #
        # self.mine_block(b)
        # print(self.blockchain)
        pass

    def receive_transaction(self, channel, message):
        """Method use when the miner receiver a message 'TRANSACTION'

        Args:
            channel:
            message:

        Returns:

        """
        print("receive transaction")
        transaction = message.content
        if transaction in self.waiting_transaction or self.blockchain.is_transaction_register(transaction):
            return
        else:
            self.add_transaction_in_queue(transaction)
            self.broadcast_transaction(transaction)
            return

    def receive_blockchain(self, channel, message):
        external_blockchain: Blockchain = message.content
        if self.blockchain.get_idx_last_block() >= external_blockchain.get_idx_last_block:
            return
        if external_blockchain.is_valid_blockchain(self.difficulty):
            self.lock.acquire()
            self.blockchain = external_blockchain
            self.lock.release()

    def receive_hi(self, channel, message: Message):
        print(f"A new server join pool : {message.source['host']}:{message.source['port']}")

    def broadcast_transaction(self, transaction: Transaction):
        """Send a message contain a transaction in broadcast

        Args:
            transaction:

        Returns:

        """
        message_in = Message("TRANSACTION", transaction, broadcast=True)
        self.channel_manager.send_message(message_in)
        print(f"Transaction broadcast -> {transaction}")

    def broadcast_blockchain(self):
        """Send a message contain a blockchain in broadcast

        Returns:

        """
        message_in = Message("BLOCKCHAIN", self.blockchain, broadcast=True)
        self.channel_manager.send_message(message_in)
        print(f"Blockchain broadcast")

    def broadcast_hi(self):
        """Send a message contain a blockchain in broadcast

        Returns:

        """
        message_in = Message("HI", broadcast=True)
        self.channel_manager.send_message(message_in)
        print(f"Hi broadcast")

    def add_transaction_in_queue(self, transaction: Transaction):
        self.lock.acquire()
        self.waiting_transaction.add(transaction)
        self.lock.release()
        return

    def delete_transaction_in_queue(self, transaction: Transaction):
        self.lock.acquire()
        self.waiting_transaction.remove(transaction)
        self.lock.release()
        return
