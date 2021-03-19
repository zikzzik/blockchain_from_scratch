import pickle
from datetime import datetime
import hashlib


class Message:
    """
    Message type allow:
        JOIN_POOL -> first message to join pool
        CONNECTION_LIST -> Contain list connection
        TRANSACTION -> send a transaction
        BLOCKCHAIN -> send a blockchain
        OK -> positive reply
        HI -> Use to say a server exist to other server

        ---
        Not implement :
        connection_list -> list of all connections knows by the miner
        error -> error reply
        test -> use only in development
    """

    allow_type_set: set = {"JOIN_POOL", "TRANSACTION", "BLOCKCHAIN", "OK", "CONNECTION_LIST", "HI"}

    def __init__(self, m_type: str, content: any = None, destination: dict = None, broadcast=False):
        """

        Args:
            m_type:
            content:
            destination: if none -> broadcast ?? to check
            broadcast:
        """
        assert m_type in Message.allow_type_set, f"'{m_type}' is incorrect message type"

        self.destination: dict = destination

        self.content: str = content
        self.m_type: str = m_type
        self.broadcast: bool = broadcast

    def to_binary(self):
        return pickle.dumps(self)

    @classmethod
    def from_binary(cls, binaries):
        return pickle.loads(binaries)

    def __str__(self):
        return f"Type : {self.m_type}, content: {self.content}"

    def add_created_at(self):
        self.created_at = datetime.now()

    def set_source(self, host: str, port: int):
        self.source: dict = {"host": host, "port": port}

    def get_source(self):
        return self.source["host"], self.source["port"]
