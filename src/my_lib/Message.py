import pickle


class Message:
    """
    Message type allow:
        join_pool -> first message to join pool
        ok -> positive reply
        error -> error reply
        test -> use only in development
    """


    def __init__(self, m_type, content=None, sender=None, receiver=None):
        self.content = content
        self.m_type = m_type
        self.sender = sender
        self.receiver = receiver

    def to_binary(self):
        return pickle.dumps(self)

    @classmethod
    def from_binary(cls, binaries):
        return pickle.loads(binaries)

    def __str__(self):
        return f"Type : {self.m_type}, content: {self.content}"

    def message_send(self):
        pass