from Crypto.PublicKey import RSA
from .Transaction import Transaction
from .TransactionRequest import TransactionRequest
from .Message import Message
from .ChannelManager import ChannelManager
from .key_utils import *
import time
import hashlib

class Wallet:
    def __init__(
        self,
        private_key_path: str,
        public_key_path: str,
        host: str = "localhost",
        port: int = 9000,
        connection_host: str = "localhost",
        connection_port: int = 8000,
    ):
        self.host = host
        self.port = port
        self.connection_host = connection_host
        self.connection_port = connection_port

        with open(private_key_path, "r") as fp:
            self.private_key = RSA.importKey(fp.read())
        with open(public_key_path, "r") as fp:
            self.public_key = RSA.importKey(fp.read())

        self.address_calculation()

    def send_token(self, receiver: str, mount: float):
        transaction = Transaction(self.address, receiver, mount, int(time.time()))
        request_transaction = TransactionRequest(transaction, self.public_key).sign_transaction(self.private_key)

        # send transaction to miner
        message = Message("REQUEST_TRANSACTION", request_transaction,
                          destination={"host": self.connection_host, "port": self.connection_port})
        channel_manager = ChannelManager(self.host, self.port)
        channel_manager.send_message(message)
        return request_transaction
    
    def address_calculation(self):
        # Inspire from bitcoin addresses creation -> https://blog.lelonek.me/how-to-calculate-bitcoin-address-in-elixir-68939af4f0e9
        str_key = self.public_key.exportKey()[27:-25].decode()
        public_key_hash = sha256(sha256(str_key))
        self.address = b58encode(public_key_hash)

    def create_key(self, public_key_path="/app/keys/1_public.pem", private_key_path="/app/keys/1_private.pem"):
        key = RSA.generate(1024)

        k = key.exportKey("PEM")
        p = key.publickey().exportKey("PEM")

        with open(private_key_path, "w") as kf:
            kf.write(k.decode())
            kf.close()

        with open(public_key_path, "w") as pf:
            pf.write(p.decode())
            pf.close()


    def check_transaction(self, transaction: Transaction):
        message = Message("CHECK_TRANSACTION", transaction,
                          destination={"host": self.connection_host, "port": self.connection_port})

        channel_manager = ChannelManager(self.host, self.port)
        channel = channel_manager.send_message(message)
        if channel is None:
            print("can't send miner")
            return
        response_message = channel.read_message()
        proof = response_message.content
        return proof.is_in_merkle_root(transaction)
