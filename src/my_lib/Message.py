import pickle
from datetime import datetime
import hashlib


class Message:
    """
    Message type allow:
        join_pool -> first message to join pool
        ok -> positive reply
        error -> error reply
        test -> use only in development
    """

    # signature ???

    def __init__(self, m_type, content=None, destination_dict: dict = None):
        """

        :param channel_manager:
        :param m_type:
        :param content:
        :param destination: if none -> broadcast
        """

        self.destination_dict = destination_dict

        self.content = content
        self.m_type = m_type

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

