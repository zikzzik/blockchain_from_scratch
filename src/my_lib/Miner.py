import random
from datetime import datetime
from .SocketConnection import SocketConnection
from .Message import Message
from .ChannelManager import ChannelManager
from .Block import Block
from .Blockchain import Blockchain
from .Transaction import Transaction
from .TransactionRequest import TransactionRequest
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
        block_size: int = 3,
        thread_miner_number: int = 2,
    ):
        self.host = host
        self.port = port
        self.difficulty = difficulty
        self.block_size = block_size
        self.lock = threading.Lock()
        self.thread_miner_number = thread_miner_number
        self.blockchain = Blockchain(self.block_size)
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
            assert (
                m_connection_list.m_type == "CONNECTION_LIST"
            ), "JOIN_POOL response message is not type 'CONNECTION_LIST'"
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
            "REQUEST_TRANSACTION": self.receive_request_transaction,
            "BLOCKCHAIN": self.receive_blockchain,
            "HI": self.receive_hi,
        }
        action_dict[message.m_type](channel, message)

    def mine_block_and_get_nonce(self, block: Block, heart_bit_interval=0.1):

        self.nonce_list = []
        for i in range(self.thread_miner_number):
            t = threading.Thread(
                target=self.mine_block_thread, args=(block, heart_bit_interval, (i, self.thread_miner_number))
            )
            t.start()

        while True:
            try:
                return [el for el in self.nonce_list if el is not None][0]
            except IndexError:
                pass

            none_count = len([el for el in self.nonce_list if el is None])
            if none_count == self.thread_miner_number:
                return None

            time.sleep(1)

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
                self.lock.acquire()
                self.nonce_list.append(block.nonce)
                self.lock.release()
                return

            if last_heart_bit + heart_bit_interval > time.time():
                if self.blockchain.get_last_block_idx() >= block.get_index():
                    self.lock.acquire()
                    self.nonce_list.append(None)
                    self.lock.release()
                    return
            nonce += strat[1]

    def start_mine(self):
        while True:
            next_block = Block(
                index=self.blockchain.get_last_block_idx() + 1,
                previous_hash=self.blockchain.get_last_block_hash(),
                block_size=self.block_size,
                timestamp=int(time.time()),
            )

            while next_block.is_full_transaction() is False:
                if len(self.waiting_transaction) > 0:
                    transaction = self.pop_transaction_in_queue()
                    if not self.blockchain.is_transaction_register(
                        transaction
                    ) and self.blockchain.is_valid_transaction(transaction):
                        next_block.add_transaction(transaction)
                else:
                    print("Wait...")
                    time.sleep(5)

            # block ready
            nonce = self.mine_block_and_get_nonce(next_block)
            if nonce is not None:
                next_block.set_nonce(nonce)
                try:
                    self.blockchain.add_block(next_block, self.lock)
                    print("add_new_block, size :", self.blockchain)
                except IndexError:
                    nonce = None

            if nonce is None:
                for transaction in next_block.transaction_list:
                    self.add_transaction_in_queue(transaction)
                print("reset block")
            else:
                self.broadcast_blockchain()

    def receive_request_transaction(self, channel, message):
        """Method use when the miner receiver a message 'REQUEST_TRANSACTION'

        Args:
            channel:
            message:

        Returns:

        """
        request_transaction = message.content
        print("receive request transaction :")
        if request_transaction.is_valid_signature:
            transaction = request_transaction.get_transaction()
        else:
            print("Bad request transaction")
            return

        if (
            transaction.is_valid() is False
            or transaction in self.waiting_transaction
            or self.blockchain.is_transaction_register(transaction)
        ):
            return
        else:
            self.add_transaction_in_queue(transaction)
            self.broadcast_request_transaction(request_transaction)
            return

    def receive_blockchain(self, channel, message):
        external_blockchain: Blockchain = message.content
        if self.blockchain.get_last_block_idx() >= external_blockchain.get_last_block_idx():
            print("received blockchain but not updated")
            return
        if external_blockchain.is_valid_blockchain(self.difficulty):
            self.lock.acquire()
            self.blockchain = external_blockchain
            self.lock.release()
            print("receive blockchain and keep it")
            print(self.blockchain)

    def receive_hi(self, channel, message: Message):
        print(f"A new server join pool : {message.source['host']}:{message.source['port']}")

    def broadcast_request_transaction(self, request_transaction: TransactionRequest):
        """Send a message contain a transaction in broadcast

        Args:
            transaction:

        Returns:

        """
        message_in = Message("REQUEST_TRANSACTION", request_transaction, broadcast=True)
        self.channel_manager.send_message(message_in)
        print(f"Request transaction broadcast -> {request_transaction}")

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

    def pop_transaction_in_queue(self):
        self.lock.acquire()
        transaction = self.waiting_transaction.pop()
        self.lock.release()
        return transaction
