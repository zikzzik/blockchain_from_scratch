import pickle
from datetime import datetime
import hashlib


class Message:
    """
    Message type allow:
        join_pool -> first message to join pool
        connection_list -> list of all connections knows by the miner
        ok -> positive reply
        error -> error reply
        test -> use only in development
    """

    # signature ???

    def __init__(self, m_type: str, content: any = None, destination: dict = None, broadcast=False):
        """

        :param channel_manager:
        :param m_type:
        :param content:
        :param destination: if none -> broadcast
        """

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

    def add_hash(self):
    #     hash_str = f"{self.m_type}_{self.content}_"
    #     self.hash = hashlib.md5(b'Hello World')
        pass

    def set_source(self, host: str, port: int):
        self.source: dict = {"host": host, "port": port}
